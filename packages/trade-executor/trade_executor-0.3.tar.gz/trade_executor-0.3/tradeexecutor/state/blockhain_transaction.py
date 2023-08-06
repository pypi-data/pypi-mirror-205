"""Tracking of blockchain transactions.

- Creating transactions and signing them from hot wallet

- Broadcasting and tracking transaction mining status

- Resolving succeed or failed transactions to succeed or failed trades

"""
import datetime
import enum
from dataclasses import dataclass, field
from typing import Optional, Any, Dict, Tuple, List

from dataclasses_json import dataclass_json, config

from eth_defi.tx import decode_signed_transaction, AssetDelta
from tradeexecutor.state.types import JSONHexAddress, JSONHexBytes


def solidity_arg_encoder(val: tuple) -> tuple:
    """JSON safe Solidity function argument encoder."""

    if type(val) not in (list, tuple):
        return val

    def _int_to_string(x):
        if type(x) == int:
            return str(x)
        if type(x) == bytes:
            return x.hex()
        elif type(x) == float:
            # Smart contracts cannot have float arguents
            raise RuntimeError(f"Cannot encode: {val}")
        return x

    return list(_int_to_string(x) for x in val)


class BlockchainTransactionType(enum.Enum):
    """What kind of transactions we generate."""

    #: Direct trade from a hot wallet
    #:
    hot_wallet = "hot_wallet"

    #: A trade tx through Enzyme's vault
    #:
    #: - Target address is the comptroller contract of the vault
    #:
    #: - The function is ComptrollerLib.callOnExtension()
    #:
    #: - The payload is integration manager call for generic adapter
    #:
    #: - The actual trade payload can be read from :py:attr:`BlockchainTransaction.details` field
    #:
    enzyme_vault = "enzyme_vault"

    #: Simulated transaction
    #:
    #: This transaction does not take place on EVM (real blockchain, unit test chain, etc).
    #: and any field like addresses or transaction hashes may not be real.
    simulated = "simulated"


@dataclass_json
@dataclass(frozen=True, slots=True)
class JSONAssetDelta:
    """JSON serialisable asset delta.

    Used for diagnostics purposes only.

    See :py:class:`eth_defi.tx.AssetDelta` for more information.
    """

    #: Address of ERC-20
    asset: str

    #: Integer as string serialisation.
    #:
    #: Because JSON cannot handle big ints.
    raw_amount: str

    @property
    def int_amount(self) -> int:
        """Convert token amount back to int."""
        return int(self.raw_amount)

    @staticmethod
    def from_asset_delta(source: AssetDelta) -> "JSONAssetDelta":
        return JSONAssetDelta(str(source.asset), str(source.raw_amount))


@dataclass_json
@dataclass(slots=True)
class BlockchainTransaction:
    """A stateful blockchain transaction.

    - The state tracks a transaction over its life cycle

    - Transactions are part of a larger logical operation (a trade)

    - Transactions can be resolved either to success or failed

    - Transaction information is easily exported to the frontend

    Transaction has (rough) four phases

    1. Preparation

    2. Signing

    3. Broadcast

    4. Confirmation
    """

    #: What kidn of internal type of this transaction is
    #:
    type: BlockchainTransactionType = BlockchainTransactionType.hot_wallet

    #: Chain id from https://github.com/ethereum-lists/chains
    chain_id: Optional[int] = None

    #: TODO: Part of signed bytes. Create an accessor.
    from_address: Optional[str] = None

    #: Contract we called. Usually the Uniswap v2 router address.
    contract_address: Optional[JSONHexAddress] = None

    #: Function we called
    function_selector: Optional[str] = None

    #: Arguments we passed to the smart contract function
    #:
    #: This is not JSON serialisable because
    #: individual arguments may contain values that are token amounts
    #: and thus outside the maximum int of JavaScript.
    #:
    args: Optional[Tuple[Any]] = field(
        default=None,
        metadata=config(
            encoder=solidity_arg_encoder,
        )
    )

    #: Blockchain bookkeeping
    tx_hash: Optional[JSONHexBytes] = None

    #: Blockchain bookkeeping
    nonce: Optional[int] = None

    #: Raw Ethereum transaction dict.
    #: Output from web3 buildTransaction()
    #:
    #: Example:
    #:
    #: `{'value': 0, 'maxFeePerGas': 1844540158, 'maxPriorityFeePerGas': 1000000000, 'chainId': 61, 'from': '0x6B49598B34B9c7FbF7C57306d0b0578676D55ffA', 'gas': 100000, 'to': '0xF2E246BB76DF876Cef8b38ae84130F4F55De395b', 'data': '0x095ea7b30000000000000000000000006d411e0a54382ed43f02410ce1c7a7c122afa6e1ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'nonce': 0}`
    #:
    details: Optional[Dict] = None

    #: Raw bytes of the signed transaction
    signed_bytes: Optional[JSONHexBytes] = None

    #: When this transaction was broadcasted
    broadcasted_at: Optional[datetime.datetime] = None

    #: Block timestamp when this tranasction was included in a block
    included_at: Optional[datetime.datetime] = None

    #: Block number when this transaction was included in a block
    block_number: Optional[int] = None

    #: Block has of the transaction where the executor saw the inclusion
    block_hash: Optional[JSONHexBytes] = None

    #: status from the tx receipt. True is success, false is revert.
    status: Optional[bool] = None

    #: Gas consumed by the tx
    realised_gas_units_consumed: Optional[int] = None

    #: Gas price for the tx in gwei
    realised_gas_price: Optional[int] = None

    #: The transaction revert reason if we manage to extract it
    revert_reason: Optional[str] = None

    #: Solidity stack trace of reverted transactions.
    #:
    #: Used in the unit testing environment with Anvil.
    #:
    #: See :py:mod:`eth_defi.trace`.
    stack_trace: Optional[str] = None

    #: List of assets this transaction touches
    #:
    #: Set in :py:class:`tradeexecutor.tx.TransactionBuilder`
    asset_deltas: List[JSONAssetDelta] = field(default_factory=list)

    def __repr__(self):
        if self.status is True:
            return f"<Tx from:{self.from_address}\n  nonce:{self.nonce}\n  to:{self.contract_address}\n  func:{self.function_selector}\n  args:{self.args}\n  succeed>\n"
        elif self.status is False:
            return f"<Tx from:{self.from_address}\n" \
                   f"    nonce:{self.nonce}\n" \
                   f"    to:{self.contract_address}\n" \
                   f"    func:{self.function_selector}\n" \
                   f"    args:{self.args}\n" \
                   f"    fail reason:{self.revert_reason}\n" \
                   f"    gas limit:{self.get_gas_limit():,}\n" \
                   f"    gas spent:{self.realised_gas_units_consumed:,}" \
                   f"    >"
        else:
            return f"<Tx from:{self.from_address}\n  nonce:{self.nonce}\n  to:{self.contract_address}\n  func:{self.function_selector}\n  args:{self.args}\n  unresolved>\n"

    def get_transaction(self) -> dict:
        """Return the transaction object as it would be in web3.py.

        Needed for :py:func:`analyse_trade_by_receipt`.
        This will reconstruct :py:class:`TypedTransaction` instance from the
        raw signed transaction bytes.
        The object will have a dict containing "data" field which we can then
        use for the trade analysis.
        """
        assert self.signed_bytes, "Not a signed transaction"
        return decode_signed_transaction(self.signed_bytes)

    def is_success(self) -> bool:
        """Transaction is success if it's succeed flag has been set."""
        return self.status

    def set_target_information(self, chain_id: int, contract_address: str, function_selector: str, args: list, details: dict):
        """Update the information on which transaction we are going to perform."""
        assert type(contract_address) == str
        assert type(function_selector) == str
        assert type(args) == list
        self.chain_id = chain_id
        self.contract_address = contract_address
        self.function_selector = function_selector
        self.args = args
        self.details = details

    def set_broadcast_information(self, nonce: int, tx_hash: str, signed_bytes: str):
        """Update the information we are going to use to broadcast the transaction."""
        assert type(nonce) == int
        assert type(tx_hash) == str
        assert type(signed_bytes) == str
        self.nonce = nonce
        self.tx_hash = tx_hash
        self.signed_bytes = signed_bytes

    def set_confirmation_information(self,
        ts: datetime.datetime,
        block_number: int,
        block_hash: str,
        realised_gas_units_consumed: int,
        realised_gas_price: int,
        status: bool,
        revert_reason: Optional[str] = None,
        stack_trace: Optional[str] = None,
        ):
        """Update the information we are going to use to broadcast the transaction."""
        assert isinstance(ts, datetime.datetime)
        assert type(block_number) == int
        assert type(block_hash) == str
        assert type(realised_gas_units_consumed) == int
        assert type(realised_gas_price) == int
        assert type(status) == bool
        self.included_at = ts
        self.block_number = block_number
        self.block_hash = block_hash
        self.realised_gas_price = realised_gas_price
        self.realised_gas_units_consumed = realised_gas_units_consumed
        self.status = status
        self.revert_reason = revert_reason
        self.stack_trace = stack_trace

    def get_planned_gas_price(self) -> int:
        """How much wei per gas unit we planned to spend on this transactions.

        Gets `maxFeePerGas` for EVM transction.

        :return:
            0 if unknown
        """
        assert self.details, "Details not set, cannot know the gas price"
        return self.details.get("maxFeePerGas", 0)

    def get_gas_limit(self) -> int:
        """Get the gas limit of the transaction.

        Gets `gas` for EVM transction.

        :return:
            0 if unknown
        """
        assert self.details, "Details not set, cannot know the gas price"
        return self.details.get("gas", 0)
