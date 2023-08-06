import datetime
from typing import Tuple

from tradeexecutor.backtest.backtest_pricing import BacktestSimplePricingModel
from tradeexecutor.state.position import TradingPosition
from tradeexecutor.state.types import USDollarAmount
from tradeexecutor.strategy.valuation import ValuationModel


class BacktestValuationModel(ValuationModel):
    """Re-value assets based on their on-chain backtest dataset price.

    Each asset is valued at its market sell price estimation.
    """

    def __init__(self, pricing_model: BacktestSimplePricingModel):
        assert pricing_model, "pricing_model missing"
        self.pricing_model = pricing_model

    def __call__(self,
                 ts: datetime.datetime,
                 position: TradingPosition) -> Tuple[datetime.datetime, USDollarAmount]:

        assert isinstance(ts, datetime.datetime)
        assert ts.second == 0, f"Timestamp sanity check failed, does not have even seconds: {ts}"

        pair = position.pair

        assert position.is_long(), "Short not supported"
        quantity = position.get_quantity()
        trade_price = self.pricing_model.get_sell_price(ts, pair, quantity)
        return ts, float(trade_price.price)


def backtest_valuation_factory(pricing_model):
    return BacktestValuationModel(pricing_model)