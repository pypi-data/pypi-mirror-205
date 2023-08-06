import logging
import datetime
import math
import warnings
from decimal import Decimal, ROUND_DOWN
from typing import Optional

import pandas as pd

from tradeexecutor.backtest.backtest_execution import BacktestExecutionModel
from tradeexecutor.backtest.backtest_routing import BacktestRoutingModel
from tradeexecutor.ethereum.uniswap_v2.uniswap_v2_routing import UniswapV2SimpleRoutingModel
from tradeexecutor.state.identifier import TradingPairIdentifier
from tradeexecutor.strategy.execution_model import ExecutionModel

from tradeexecutor.state.types import USDollarPrice
from tradeexecutor.strategy.pricing_model import PricingModel
from tradeexecutor.strategy.trade_pricing import TradePricing
from tradeexecutor.strategy.routing import RoutingModel
from tradeexecutor.strategy.trading_strategy_universe import TradingStrategyUniverse, translate_trading_pair
from tradingstrategy.candle import GroupedCandleUniverse
from tradingstrategy.timebucket import TimeBucket

logger = logging.getLogger(__name__)


class BacktestSimplePricingModel(PricingModel):
    """Look up the historical prices.

    - Open price of the price candle at the timestamp,
      or closest earlier timestamp is used

    - Different pricing model can be used for rebalances (more coarse)
      and stop losses (more granular)

    - This is a simple model and does not use liquidity data
      for the price impact estimation

    - We provide `data_delay_tolerance` to deal with potential
      gaps in price data
    """

    def __init__(self,
                candle_universe: GroupedCandleUniverse,
                routing_model: RoutingModel,
                data_delay_tolerance=pd.Timedelta("2d"),
                candle_timepoint_kind="open",
                very_small_amount=Decimal("0.10"),
                time_bucket: Optional[TimeBucket] = None,
                allow_missing_fees=False,
        ):
        """

        :param candle_universe:
            Candles where our backtesing date comes from

        :param routing_model:
            How do we route trades between different pairs
            TODO: Now ignored

        :param data_delay_tolerance:
            How long time gaps we allow in the backtesting data
            before aborting the backtesting with an exception.
            This is an safety check for bad data.

            Sometimes there cannot be trades for days
            if the blockchain has been halted,
            and thus no price data available.

        :param candle_timepoint_kind:
            Do we use opening or closing price in backtesting

        :param very_small_amount:
            What kind o a test amount we do use for a trade
            when we do not know the actual size of the trade.

        :param time_bucket:
            The granularity of the price data.

            Currently used for diagnostics and debug only.

        :param allow_missing_fees:
            Allow trading pairs with missing fee information.

            All trading pairs should have good fee information by default,
            unless dealing with legacy tests.

        """

        # TODO: Remove later - now to support some old code111
        if isinstance(candle_universe, TradingStrategyUniverse):
            candle_universe = candle_universe.universe.candles

        assert isinstance(candle_universe, GroupedCandleUniverse), f"Got candles in wrong format: {candle_universe.__class__}"

        self.candle_universe = candle_universe
        self.very_small_amount = very_small_amount
        self.routing_model = routing_model
        self.candle_timepoint_kind = candle_timepoint_kind
        self.data_delay_tolerance = data_delay_tolerance
        self.time_bucket = time_bucket
        self.allow_missing_fees = allow_missing_fees

    def __repr__(self):
        return f"<BacktestSimplePricingModel bucket: {self.time_bucket}, candles: {self.candle_universe}>"

    def get_pair_for_id(self, internal_id: int) -> Optional[TradingPairIdentifier]:
        """Look up a trading pair.

        Useful if a strategy is only dealing with pair integer ids.
        """
        warnings.warn("Do not use internal ids as they are not stable ids."
                      "Instead use chain id + address tuples")

        pair = self.universe.pairs.get_pair_by_id(internal_id)
        if not pair:
            return None
        return translate_trading_pair(pair)

    def check_supported_quote_token(self, pair: TradingPairIdentifier):
        assert pair.quote.address == self.routing_model.reserve_token_address, f"Quote token {self.routing_model.reserve_token_address} not supported for pair {pair}, pair tokens are {pair.base.address} - {pair.quote.address}"

    def get_sell_price(self,
                       ts: datetime.datetime,
                       pair: TradingPairIdentifier,
                       quantity: Optional[Decimal]) -> TradePricing:

        if quantity:
            assert quantity > 0, f"Cannot sell negative amounts: {quantity} {pair}"

        # TODO: Include price impact
        pair_id = pair.internal_id

        mid_price, delay = self.candle_universe.get_price_with_tolerance(
            pair_id,
            ts,
            tolerance=self.data_delay_tolerance,
            kind=self.candle_timepoint_kind)

        pair_fee = self.get_pair_fee(ts, pair)

        if pair_fee:
            reserve = float(quantity) * mid_price
            lp_fee = float(reserve) * pair_fee

            # Move price below mid price
            price = mid_price * (1 - pair_fee)

            assert lp_fee > 0, f"Got bad fee: {pair} {quantity}: {lp_fee}"

        else:
            # Fee information not available
            if not self.allow_missing_fees:
                raise AssertionError(f"Pair lacks fee information: {pair}")

            price = mid_price
            lp_fee = None

        return TradePricing(
            price=float(price),
            mid_price=float(mid_price),
            lp_fee=lp_fee,
            pair_fee=pair_fee,
            market_feed_delay=delay.to_pytimedelta(),
            side=False,
            path=[pair]
        )

    def get_buy_price(self,
                       ts: datetime.datetime,
                       pair: TradingPairIdentifier,
                       reserve: Optional[Decimal]) -> TradePricing:
        """Get the price for a buy transaction."""

        assert reserve is not None and reserve > 0, f"For a buy estimation, please fill in the allocated reserve amount for: {pair}. Got reserve: {reserve}"

        # TODO: Include price impact
        pair_id = pair.internal_id

        mid_price, delay = self.candle_universe.get_price_with_tolerance(
            pair_id,
            ts,
            tolerance=self.data_delay_tolerance,
            kind=self.candle_timepoint_kind,
        )

        assert mid_price not in (0, math.nan), f"Got bad mid price: {mid_price}"

        pair_fee = self.get_pair_fee(ts, pair)

        if pair_fee is not None:
            lp_fee = float(reserve) * pair_fee

            # Move price above mid price
            price = mid_price * (1 + pair_fee)

            assert lp_fee > 0, f"Got bad fee: {pair} {reserve}: {lp_fee}"
        else:
            # Fee information not available
            if not self.allow_missing_fees:
                raise AssertionError(f"Pair lacks fee information: {pair}")
            lp_fee = None
            price = mid_price

        assert price not in (0, math.nan) and price > 0, f"Got bad price: {price}"

        return TradePricing(
            price=float(price),
            mid_price=float(mid_price),
            lp_fee=lp_fee,
            pair_fee=pair_fee,
            market_feed_delay=delay.to_pytimedelta(),
            side=True,
            path=[pair]
        )

    def get_mid_price(self,
                      ts: datetime.datetime,
                      pair: TradingPairIdentifier) -> USDollarPrice:
        """Get the mid price by the candle."""
        pair_id = pair.internal_id

        price, delay = self.candle_universe.get_price_with_tolerance(
            pair_id,
            ts,
            tolerance=self.data_delay_tolerance,
            kind=self.candle_timepoint_kind,
        )
        return float(price)

    def quantize_base_quantity(self, pair: TradingPairIdentifier, quantity: Decimal, rounding=ROUND_DOWN) -> Decimal:
        """Convert any base token quantity to the native token units by its ERC-20 decimals."""
        assert isinstance(pair, TradingPairIdentifier)
        decimals = pair.base.decimals
        return Decimal(quantity).quantize((Decimal(10) ** Decimal(-decimals)), rounding=ROUND_DOWN)

    def get_pair_fee(self,
                     ts: datetime.datetime,
                     pair: TradingPairIdentifier,
                     ) -> Optional[float]:
        """Figure out the fee from a pair or a routing."""
        if pair.fee:
            return pair.fee

        return self.routing_model.get_default_trading_fee()


def backtest_pricing_factory(
        execution_model: ExecutionModel,
        universe: TradingStrategyUniverse,
        routing_model: UniswapV2SimpleRoutingModel) -> BacktestSimplePricingModel:

    assert isinstance(universe, TradingStrategyUniverse)
    assert isinstance(execution_model, BacktestExecutionModel), f"Execution model not compatible with this execution model. Received {execution_model}"
    assert isinstance(routing_model, (BacktestRoutingModel, UniswapV2SimpleRoutingModel)), f"This pricing method only works with Uniswap routing model, we received {routing_model}"

    return BacktestSimplePricingModel(
        universe.universe.candles,
        routing_model)

