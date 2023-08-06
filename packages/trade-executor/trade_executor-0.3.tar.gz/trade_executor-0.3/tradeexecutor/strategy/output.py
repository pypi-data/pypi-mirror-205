"""Helpers for outputting strategy execution information to Python logging and Discord."""

from io import StringIO
from typing import List, Iterable

from tradeexecutor.state.portfolio import Portfolio
from tradeexecutor.state.position import TradingPosition
from tradeexecutor.state.trade import TradeExecution

#: See setup_discord_logging()
DISCORD_BREAK_CHAR = "…"


def format_trade(portfolio: Portfolio, trade: TradeExecution) -> List[str]:
    """Write a trade status line to logs.

    :return: List of log lines
    """
    pair = trade.pair
    if pair.info_url:
        link = pair.info_url
    else:
        link = ""

    if trade.is_buy():
        trade_type = "Buy"
    else:
        trade_type = "Sell"

    existing_position = portfolio.get_existing_open_position_by_trading_pair(trade.pair)
    if existing_position:
        amount = abs(trade.planned_quantity / existing_position.get_net_quantity())
        existing_text = f", {amount*100:,.2f}% of existing position"
    else:
        existing_text = ""

    lines = [
        f"{trade_type:5} #{trade.trade_id} {pair.get_human_description()} ${trade.get_planned_value():,.2f} ({abs(trade.get_position_quantity())} {pair.base.token_symbol}){existing_text}",
    ]

    if link:
        lines.append(f"      link: {link}")

    return lines


def format_position(position: TradingPosition, up_symbol="🌲", down_symbol="🔻") -> List[str]:
    """Write a position status line to logs.

    Position can be open/closed.

    :return: List of log lines
    """
    symbol = up_symbol if position.get_total_profit_percent() >= 0 else down_symbol
    if position.pair.info_url:
        link = position.pair.info_url
    else:
        link = ""

    lines =[
        f"{symbol} #{position.position_id} {position.pair.get_human_description()} size:${position.get_value():,.2f}, profit:{position.get_total_profit_percent():.2f}% ({position.get_total_profit_usd():,.4f} USD)"
    ]

    if position.has_executed_trades():
        price_diff = position.get_current_price() - position.get_opening_price()
        lines.append(f"   current price:${position.get_current_price():,.8f}, open price:${position.get_opening_price():,.8f}, diff:{price_diff:,.8f} USD")
        lines.append(f"   last tx:${position.get_last_tx_hash()}")

    if position.is_frozen():
        last_trade = "buy" if position.get_last_trade().is_buy() else "sell"
        lines.append(f"   last trade: {last_trade}, freeze reason: {position.get_freeze_reason()}")

    if link:
        lines.append(f"   link: {link}")

    return lines


def output_positions(positions: Iterable[TradingPosition], buf: StringIO, empty_message="No positions", break_after=4):
    """Write info on multiple trading positions formatted for Python logging system.

    :break_after:
        Insert Discord message break after this many positions to avoid
        chopped Discord messages.

    :return: A plain text string as a log message, suitable for Discord logging
    """
    positions = list(positions)

    if len(positions) > 0:
        position: TradingPosition

        for idx, position in enumerate(positions):
            for line in format_position(position):
                print("    " + line, file=buf)

            if (idx + 1) % break_after == 0:
                # Discord message break
                print(DISCORD_BREAK_CHAR, file=buf)
            else:
                # Line break
                print("", file=buf)

    else:
        print(f"    {empty_message}", file=buf)
    return buf.getvalue()


def output_trades(trades: List[TradeExecution], portfolio: Portfolio, buf: StringIO):
    """Write trades to the output logs."""
    for t in trades:
        for line in format_trade(portfolio, t):
            print("    " + line, file=buf)
        print("", file=buf)
