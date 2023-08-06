"""Strategy initialisation using factory design pattern.

Bind loaded strategies to the execution environment.
"""

from typing import Protocol, Optional

from contextlib import AbstractContextManager

from tradingstrategy.client import Client

from tradeexecutor.strategy.sync_model import SyncMethodV0, SyncModel
from tradeexecutor.strategy.approval import ApprovalModel
from tradeexecutor.strategy.description import StrategyExecutionDescription
from tradeexecutor.strategy.execution_model import ExecutionModel
from tradeexecutor.strategy.pricing_model import PricingModelFactory
from tradeexecutor.strategy.routing import RoutingModel
from tradeexecutor.strategy.valuation import ValuationModelFactory



class StrategyFactory(Protocol):
    """A callable that creates a new strategy when loaded from an external script."""

    # Only accept kwargs as per https://www.python.org/dev/peps/pep-3102/
    def __call__(
        *ignore,
        execution_model: ExecutionModel,
        sync_model: SyncModel,
        pricing_model_factory: PricingModelFactory,
        valuation_model_factory: ValuationModelFactory,
        client: Optional[Client],
        timed_task_context_manager: AbstractContextManager,
        approval_model: ApprovalModel,
        routing_model: Optional[RoutingModel] = None,
        **kwargs) -> StrategyExecutionDescription:
        """

        :param ignore:

        :param execution_model:
            TODO

        :param sync_method:
            TODO

        :param pricing_model_factory:
            TODO

        :param valuation_model_factory:
            TODO

        :param client:
            TODO

        :param timed_task_context_manager:
            TODO

        :param approval_model:
            TODO

        :param routing_model:
            Strategy factory can create its own routing model, or accept the passed one.
            Passing it here is mainly used in the tests as a shortcut.

        :param kwargs:
        :return:
        """


