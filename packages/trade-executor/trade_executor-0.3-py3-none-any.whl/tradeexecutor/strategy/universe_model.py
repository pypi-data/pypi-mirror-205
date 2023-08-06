"""Construct the trading universe for the strategy."""
import abc
import datetime
from dataclasses import dataclass
from typing import List, Optional, Collection

from tradingstrategy.timebucket import TimeBucket

from tradeexecutor.state.identifier import AssetIdentifier
from tradeexecutor.strategy.execution_context import ExecutionMode


class DataTooOld(Exception):
    """We try to execute live trades, but our data is too old for us to work with."""


@dataclass
class StrategyExecutionUniverse:
    """Represents whatever data a strategy needs to have in order to make trading decisions.

    Any strategy specific subclass will handle candle/liquidity datasets.
    """

    #: The list of reserve assets used in this strategy.
    #:
    #: Currently we support only one reserve asset per strategy, though in the
    #: future there can be several.
    #:
    #: Usually return the list of a BUSD/USDC/similar stablecoin.
    #:
    #: TODO: Migrate to Set[] in all the code
    reserve_assets: Collection[AssetIdentifier]

    def __post_init__(self):
        # Check that reserve assets look good
        for asset in self.reserve_assets:
            assert asset.token_symbol, f"Missing token symbol {asset}"
            assert asset.decimals, f"Missing token decimals {asset}"

    def get_reserve_asset(self) -> AssetIdentifier:
        """Get the default reserve asset.

        :raise AssertionError:
            If we have multiple reserve assets (unsupported)
        """
        assert len(self.reserve_assets) == 1
        return self.reserve_assets[0]


@dataclass
class UniverseOptions:
    """Options that we can pass for the trading strategy universe creation.

    These can be given on the command line, or from the parent
    execution context. It allows to override parameters
    given in the strategy file easily without need to edit the file.

    The most common use case is to speed up backtesting by
    decreasing the stop loss check frequency.

    The default options do not override anything:

    .. code-block:: shell

        universe_options = UniverseOptions()

    See :ref:`command-line-backtest` how these options are used.
    """

    candle_time_bucket_override: Optional[TimeBucket] = None

    stop_loss_time_bucket_override: Optional[TimeBucket] = None


class UniverseModel(abc.ABC):
    """Create and manage trade universe.

    On a live execution, the trade universe is reconstructor for the every tick,
    by refreshing the trading data from the server.
    """

    def preload_universe(self, universe_options: UniverseOptions) -> StrategyExecutionUniverse:
        """Triggered before backtesting execution.

        - Load all datasets with progress bar display

        - Data is saved in FS cache

        - Not triggered in live trading, as universe changes between cycles

        :param universe_options:
            Options to override universe loading parameters from the strategy file
        """

    @abc.abstractmethod
    def construct_universe(self,
                           ts: datetime.datetime,
                           mode: ExecutionMode,
                           universe_options: UniverseOptions) -> StrategyExecutionUniverse:
        """On each strategy tick, refresh/recreate the trading universe for the strategy.

        This is called in mainloop before the strategy tick. It needs to download
        any data updates since the last tick.

        :param mode:
            Are we live trading or backtesting.

        :param universe_options:
            Override any parameters for universe data.
            Most useful for making stop loss data checks less frequent,
            speeding up the backtesting.
        """

    def check_data_age(self, ts: datetime.datetime, universe: StrategyExecutionUniverse, best_before_duration: datetime.timedelta):
        """Check if our data is up-to-date and we do not have issues with feeds.

        Ensure we do not try to execute live trades with stale data.

        :raise DataTooOld: in the case data is too old to execute.
        """


class StaticUniverseModel(UniverseModel):
    """Universe that never changes and all assets are in in-process memory.

    Only useful for testing, because
    - any real trading pair universe is deemed to change
    - trade executor is deemed to go down and up again
    """

    def __init__(self, universe: StrategyExecutionUniverse):
        assert isinstance(universe, StrategyExecutionUniverse)
        self.universe = universe

    def construct_universe(self, ts: datetime.datetime, live: bool, universe_options: UniverseOptions) -> StrategyExecutionUniverse:
        """Always return the same universe copy - there is no refresh."""
        return self.universe

