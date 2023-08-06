"""Route trades to different Uniswap v2 like exchanges."""

import logging
from collections import defaultdict
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod

from eth_typing import ChecksumAddress
from web3.contract.contract import ContractFunction

from eth_defi.tx import AssetDelta
from tradeexecutor.state.types import BPS
from web3 import Web3
from web3.contract import Contract

from eth_defi.abi import get_deployed_contract
from eth_defi.token import fetch_erc20_details
from eth_defi.uniswap_v2.deployment import UniswapV2Deployment
from eth_defi.uniswap_v3.deployment import UniswapV3Deployment

from tradeexecutor.ethereum.tx import HotWalletTransactionBuilder, TransactionBuilder
from tradeexecutor.state.blockhain_transaction import BlockchainTransaction
from tradeexecutor.state.identifier import TradingPairIdentifier, AssetIdentifier
from tradeexecutor.strategy.routing import RoutingState
from tradingstrategy.pair import PandasPairUniverse



logger = logging.getLogger(__name__)


class OutOfBalance(Exception):
    """Did not have enough tokens"""


deployment_types = UniswapV2Deployment | UniswapV3Deployment


class EthereumRoutingState(RoutingState):
    """Manage transaction building for multiple Uniswap trades.

    - Lifespan is one rebalance - remembers already made approvals

    - Web3 connection and hot wallet

    - Approval tx creation

    - Swap tx creation

    Manage the state of already given approvals here,
    so that we do not do duplicates.

    The approvals are not persistent in the executor state,
    but are specific for each cycle.
    """

    def __init__(self,
                 pair_universe: PandasPairUniverse,
                 tx_builder: Optional[TransactionBuilder] = None,
                 swap_gas_limit=2_000_000,
                 web3: Optional[Web3] = None,
                 ):
        """

        :param pair_universe:
            Pairs we trade

        :param tx_builder:
            For creating trade transactions.

            Can be set to None on DummyExecutionModel.

        :param web3:
            Use for routing smart contract reads.

            Given when `tx_builder` is not present.

        :param swap_gas_limit:
            What is the max gas we are willing to pay for a swap.

        """

        # Parent does not need to be called,
        # TODO: fix parent API signature later,
        # because full universe is not needed
        self.pair_universe = pair_universe

        if tx_builder is not None:
            self.tx_builder = tx_builder
            self.web3 = self.tx_builder.web3
        else:
            # DummyExecution model does not have a wallet
            # and cannot build transactions
            self.tx_builder = None
            self.hot_wallet = None
            self.web3 = web3

        # router -> erc-20 mappings
        self.approved_routes = defaultdict(set)
        self.swap_gas_limit = swap_gas_limit
        
    @abstractmethod
    def get_uniswap_for_pair():
        """Get a router for a trading pair."""
    
    @abstractmethod
    def trade_on_router_two_way(self,
            uniswap: deployment_types,
            target_pair: TradingPairIdentifier,
            reserve_asset: AssetIdentifier,
            reserve_amount: int,
            max_slippage: float,
            check_balances: False,
            asset_deltas: Optional[List[AssetDelta]] = None,
        ):
        """Prepare the actual swap. Same for Uniswap V2 and V3."""
        
    @abstractmethod
    def trade_on_router_three_way(self,
            uniswap: deployment_types,
            target_pair: TradingPairIdentifier,
            intermediary_pair: TradingPairIdentifier,
            reserve_asset: AssetIdentifier,
            reserve_amount: int,
            max_slippage: float,
            check_balances: False,
            asset_deltas: Optional[List[AssetDelta]] = None,
        ):
        """Prepare the actual swap for three way trade."""

    def is_route_approved(self, router_address: str):
        return router_address in self.approved_routes

    def mark_router_approved(self, token_address, router_address):
        self.approved_routes[router_address].add(token_address)

    def is_approved_on_chain(self, token_address: str, router_address: str) -> bool:
        erc_20 = get_deployed_contract(self.web3, "ERC20MockDecimals.json", token_address)
        # Assume allowance is always infinity
        return erc_20.functions.allowance.call(self.tx_builder.get_token_delivery_address(), router_address) > 0

    def check_has_enough_tokens(
            self,
            erc_20: Contract,
            amount: int,
    ):
        """Check we have enough buy side tokens to do a trade.

        This might not be the case if we are preparing transactions ahead of time and
        sell might have not happened yet.
        """
        address = self.tx_builder.get_erc_20_balance_address()
        balance = erc_20.functions.balanceOf(address).call()
        if balance < amount:
            token_details = fetch_erc20_details(
                erc_20.w3,
                erc_20.address,
            )
            d_balance = token_details.convert_to_decimals(balance)
            d_amount = token_details.convert_to_decimals(amount)
            raise OutOfBalance(f"Address {address} does not have enough {token_details} tokens to trade. Need {d_amount}, has {d_balance}")

    def ensure_token_approved(self,
                              token_address: str,
                              router_address: str) -> List[BlockchainTransaction]:
        """Make sure we have ERC-20 approve() for the trade

        - Infinite approval on-chain

        - ...or previous approval in this state,

        :param token_address:
        :param router_address:

        :return: Create 0 or 1 transactions if needs to be approved
        """

        assert self.tx_builder is not None

        if token_address in self.approved_routes[router_address]:
            # Already approved for this cycle in previous trade
            return []

        erc_20 = get_deployed_contract(self.web3, "ERC20MockDecimals.json", Web3.to_checksum_address(token_address))

        # Set internal state we are approved
        self.mark_router_approved(token_address, router_address)

        approve_address = self.tx_builder.get_token_delivery_address()

        if erc_20.functions.allowance(approve_address, router_address).call() > 0:
            # already approved in previous execution cycle
            return []
        
        # Create infinite approval
        tx = self.tx_builder.sign_transaction(
            erc_20,
            erc_20.functions.approve(router_address, 2**256-1),
            gas_limit=None,  # For approve, assume it cannot take more than 100k gas
            gas_price_suggestion=None,
            asset_deltas=[],
        )

        return [tx]
    
    def create_signed_transaction(
            self,
            contract: Contract,
            swap_func: ContractFunction,
            gas_limit: int,
            asset_deltas: List[AssetDelta]):
        signed_tx = self.tx_builder.sign_transaction(
            contract,
            swap_func,
            gas_limit,
            gas_price_suggestion=None,
            asset_deltas=asset_deltas,
        )
        return [signed_tx]
    
    @staticmethod
    def validate_pairs(target_pair, intermediary_pair):
        """Check we can chain two pairs
        """
        assert intermediary_pair.base == target_pair.quote, f"Could not hop from intermediary {intermediary_pair} -> destination {target_pair}"

        assert target_pair.exchange_address, f"Target pair {target_pair} missing exchange information"
        assert intermediary_pair.exchange_address, f"Intermediary pair {intermediary_pair} missing exchange information"

        # Check routing happens on the same exchange
        assert intermediary_pair.exchange_address.lower() == target_pair.exchange_address.lower()
        
    @staticmethod
    def validate_exchange(target_pair, intermediary_pair):
        """Check routing happens on the same exchange"""
        assert intermediary_pair.exchange_address.lower() == target_pair.exchange_address.lower()
    
    
def route_tokens(
        trading_pair: TradingPairIdentifier,
        intermediate_pair: Optional[TradingPairIdentifier],
)-> Tuple[ChecksumAddress, ChecksumAddress, Optional[ChecksumAddress]]:
    """Convert trading pair route to physical token addresses.
    """

    if intermediate_pair is None:
        return (Web3.to_checksum_address(trading_pair.base.address),
            Web3.to_checksum_address(trading_pair.quote.address),
            None)

    return (Web3.to_checksum_address(trading_pair.base.address),
        Web3.to_checksum_address(intermediate_pair.quote.address),
        Web3.to_checksum_address(trading_pair.quote.address))


def get_base_quote(web3: Web3, target_pair: TradingPairIdentifier, reserve_asset: AssetIdentifier, error_msg: str = None):
        """Get base and quote token from the pair and reserve asset. Called in parent class (RoutingState) with error_msg.
        
        See: https://tradingstrategy.ai/docs/programming/market-data/trading-pairs.html
        
        :param target_pair: Pair to be traded
        :param reserver_asset: Asset to be kept as reserves
        :returns: (base_token: Contract, quote_token: Contract)
        :param error_msg:
            Only provide this argument if error message includes external info such as an intermediary pair
        """
        if error_msg is None:
            error_msg = f"Cannot route trade through {target_pair}"
        
        if reserve_asset == target_pair.quote:
            # Buy with e.g. BUSD
            base_token = get_token_for_asset(web3, target_pair.base)
            quote_token = get_token_for_asset(web3, target_pair.quote)
            
        elif reserve_asset == target_pair.base:
            # Sell, flip the direction
            base_token = get_token_for_asset(web3, target_pair.quote)
            quote_token = get_token_for_asset(web3, target_pair.base)
            
        else:
            raise RuntimeError(error_msg)
        
        return base_token, quote_token


def get_base_quote_intermediary(web3: Web3, target_pair: TradingPairIdentifier, intermediary_pair: TradingPairIdentifier, reserve_asset: AssetIdentifier):
        
        if reserve_asset == intermediary_pair.quote:
            # Buy BUSD -> BNB -> Cake
            base_token = get_token_for_asset(web3, target_pair.base)
            quote_token = get_token_for_asset(web3, intermediary_pair.quote)
            intermediary_token = get_token_for_asset(web3, intermediary_pair.base)
        elif reserve_asset == target_pair.base:
            # Sell, Cake -> BNB -> BUSD
            base_token = get_token_for_asset(web3, intermediary_pair.quote)  # BUSD
            quote_token = get_token_for_asset(web3, target_pair.base)  # Cake
            intermediary_token = get_token_for_asset(web3, intermediary_pair.base)  # BNB
        else:
            raise RuntimeError(f"Cannot trade {target_pair} through {intermediary_pair}")
        return base_token,quote_token,intermediary_token

    
def get_token_for_asset(web3: Web3, asset: AssetIdentifier) -> Contract:
    """Get ERC-20 contract proxy."""
    erc_20 = get_deployed_contract(web3, "ERC20MockDecimals.json", Web3.to_checksum_address(asset.address))
    return erc_20