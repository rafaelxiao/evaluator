from decimal import Decimal
from typing import List, Optional, Dict
from collections import defaultdict

from ..models.performance import Performance
from ..models.session_stats import SessionStats
from ..models.comparison import PerformanceComparison


class PerformanceFormatter:
    @staticmethod
    def format_decimal(value: Decimal, decimals: int = 2) -> str:
        return f"{float(value):,.{decimals}f}"

    @staticmethod
    def format_pct(value: float, decimals: int = 2) -> str:
        return f"{value:.{decimals}f}%"

    @staticmethod
    def print_separator(char: str = "=", length: int = 70):
        print(char * length)

    @staticmethod
    def print_header(title: str):
        PerformanceFormatter.print_separator()
        print(title)
        PerformanceFormatter.print_separator()

    @staticmethod
    def calculate_base_amount(sessions: List[SessionStats]) -> Decimal:
        if not sessions:
            return Decimal("0")
        for session in sessions:
            if session.start_cash > 0:
                return session.start_cash
        return Decimal("0")

    @staticmethod
    def print_performance_metrics(performance: Performance):
        if not performance:
            print("No performance data available.")
            return

        PerformanceFormatter.print_header("PERFORMANCE METRICS - OVERVIEW")
        print(f"{'Metric':<35} {'Value':>25}")
        PerformanceFormatter.print_separator("-", 70)
        print(f"{'Net Profit:':<35} {PerformanceFormatter.format_decimal(performance.net_profit):>25}")
        print(f"{'Net Profit %:':<35} {PerformanceFormatter.format_pct(performance.net_profit_pct):>25}")
        print(f"{'Initial Cash:':<35} {PerformanceFormatter.format_decimal(performance.initial_cash):>25}")
        print(f"{'Final Value:':<35} {PerformanceFormatter.format_decimal(performance.final_value):>25}")
        print()

        PerformanceFormatter.print_header("PERFORMANCE METRICS - TRADES")
        print(f"{'Metric':<35} {'Value':>25}")
        PerformanceFormatter.print_separator("-", 70)
        print(f"{'Total Trades:':<35} {performance.total_trades:>25}")
        print(f"{'Open Positions:':<35} {performance.open_positions:>25}")
        print(f"{'Winning Trades:':<35} {performance.winning_trades:>25}")
        print(f"{'Losing Trades:':<35} {performance.losing_trades:>25}")
        print(f"{'Win Rate:':<35} {PerformanceFormatter.format_pct(performance.win_rate):>25}")
        print()

        PerformanceFormatter.print_header("PERFORMANCE METRICS - RETURNS")
        print(f"{'Metric':<35} {'Value':>25}")
        PerformanceFormatter.print_separator("-", 70)
        print(f"{'Sharpe Ratio:':<35} {performance.sharpe_ratio:>25.4f}")
        print(f"{'Sortino Ratio:':<35} {performance.sortino_ratio:>25.4f}")
        print(f"{'Calmar Ratio:':<35} {performance.calmar_ratio:>25.4f}")
        print(f"{'Max Drawdown:':<35} {PerformanceFormatter.format_decimal(performance.max_drawdown):>25}")
        print(f"{'Max Drawdown Duration (bars):':<35} {performance.max_drawdown_duration_bars:>25}")
        print()

        PerformanceFormatter.print_header("PERFORMANCE METRICS - SINGLE TRADE")
        print(f"{'Metric':<35} {'Value':>25}")
        PerformanceFormatter.print_separator("-", 70)
        print(f"{'Max Single Win:':<35} {PerformanceFormatter.format_decimal(performance.max_single_win):>25}")
        print(f"{'Max Single Loss:':<35} {PerformanceFormatter.format_decimal(performance.max_single_loss):>25}")
        print(f"{'Max Single Win %:':<35} {PerformanceFormatter.format_pct(performance.max_single_win_pct):>25}")
        print(f"{'Max Single Loss %:':<35} {PerformanceFormatter.format_pct(performance.max_single_loss_pct):>25}")
        print(f"{'Average Win:':<35} {PerformanceFormatter.format_decimal(performance.avg_win):>25}")
        print(f"{'Average Loss:':<35} {PerformanceFormatter.format_decimal(performance.avg_loss):>25}")
        print(f"{'Average Win %:':<35} {PerformanceFormatter.format_pct(performance.avg_win_pct):>25}")
        print(f"{'Average Loss %:':<35} {PerformanceFormatter.format_pct(performance.avg_loss_pct):>25}")
        print(f"{'Odds Ratio (Win/Loss):':<35} {performance.odds_ratio:>25.4f}")
        print(f"{'Total Win Amount:':<35} {PerformanceFormatter.format_decimal(performance.total_win):>25}")
        print(f"{'Total Loss Amount:':<35} {PerformanceFormatter.format_decimal(performance.total_loss):>25}")
        print()

        PerformanceFormatter.print_header("PERFORMANCE METRICS - COMMISSION")
        print(f"{'Metric':<35} {'Value':>25}")
        PerformanceFormatter.print_separator("-", 70)
        print(f"{'Total Commission:':<35} {PerformanceFormatter.format_decimal(performance.total_commission):>25}")
        print(f"{'Commission Loss %:':<35} {PerformanceFormatter.format_pct(performance.commission_loss_pct):>25}")
        print()

        PerformanceFormatter.print_header("PERFORMANCE METRICS - TOP CONTRIBUTORS")
        print(f"{'Metric':<35} {'Value':>25}")
        PerformanceFormatter.print_separator("-", 70)
        print(f"{'Top 1% Win Contribution:':<35} {PerformanceFormatter.format_pct(performance.top_1pct_win_pct):>25}")
        print(f"{'Top 5% Win Contribution:':<35} {PerformanceFormatter.format_pct(performance.top_5pct_win_pct):>25}")
        print(f"{'Top 10% Win Contribution:':<35} {PerformanceFormatter.format_pct(performance.top_10pct_win_pct):>25}")
        print(f"{'Top 20% Win Contribution:':<35} {PerformanceFormatter.format_pct(performance.top_20pct_win_pct):>25}")
        print()
        print(f"{'Top 1% Loss Contribution:':<35} {PerformanceFormatter.format_pct(performance.top_1pct_loss_pct):>25}")
        print(f"{'Top 5% Loss Contribution:':<35} {PerformanceFormatter.format_pct(performance.top_5pct_loss_pct):>25}")
        print(f"{'Top 10% Loss Contribution:':<35} {PerformanceFormatter.format_pct(performance.top_10pct_loss_pct):>25}")
        print(f"{'Top 20% Loss Contribution:':<35} {PerformanceFormatter.format_pct(performance.top_20pct_loss_pct):>25}")
        print()

    @staticmethod
    def print_account_summary(sessions: List[SessionStats]):
        if not sessions:
            print("No session data available.")
            return

        first_session = sessions[0]
        last_session = sessions[-1]
        base_amount = PerformanceFormatter.calculate_base_amount(sessions)

        PerformanceFormatter.print_header("ACCOUNT SUMMARY")
        print(f"{'Total Sessions:':<30} {len(sessions)}")
        print(f"{'First Session:':<30} {first_session.session}")
        print(f"{'Last Session:':<30} {last_session.session}")
        print(f"{'Base Amount (Initial):':<30} {PerformanceFormatter.format_decimal(base_amount)}")
        print(f"{'Final Cash:':<30} {PerformanceFormatter.format_decimal(last_session.end_cash)}")
        print(f"{'Total Cash Change:':<30} {PerformanceFormatter.format_decimal(last_session.end_cash - first_session.start_cash)}")
        print()

    @staticmethod
    def print_session_details(sessions: List[SessionStats], base_amount: Optional[Decimal] = None):
        if not sessions:
            print("No session data available.")
            return

        if base_amount is None:
            base_amount = PerformanceFormatter.calculate_base_amount(sessions)

        PerformanceFormatter.print_header("SESSION DETAILS")
        print(f"{'Session':<12} {'Start Cash':>14} {'End Cash':>14} {'Adj PnL':>14} {'Traded':>8} {'Held':>6}")
        PerformanceFormatter.print_separator("-", 70)

        total_pnl = Decimal("0")
        first_session = True

        for session in sessions:
            if first_session:
                pnl = session.profit_loss - base_amount + session.start_cash
                first_session = False
            else:
                pnl = session.profit_loss

            total_pnl += pnl
            num_traded = len([p for p in session.end_positions if p.trade_count > 0])
            num_held = len([p for p in session.end_positions if p.end_volume > 0])
            print(
                f"{session.session:<12} "
                f"{PerformanceFormatter.format_decimal(session.start_cash):>14} "
                f"{PerformanceFormatter.format_decimal(session.end_cash):>14} "
                f"{PerformanceFormatter.format_decimal(pnl):>14} "
                f"{num_traded:>8} "
                f"{num_held:>6}"
            )

        PerformanceFormatter.print_separator("-", 70)
        print(f"{'TOTAL':<12} {'':>14} {'':>14} {PerformanceFormatter.format_decimal(total_pnl):>14} {'':>10}")
        print()

    @staticmethod
    def print_symbol_breakdown(sessions: List[SessionStats]):
        if not sessions:
            print("No session data available.")
            return

        symbol_pnl: Dict[str, Decimal] = defaultdict(Decimal)
        symbol_trades: Dict[str, int] = defaultdict(int)

        for session in sessions:
            for pos in session.end_positions:
                symbol_pnl[pos.symbol] += pos.realized_profit
                symbol_trades[pos.symbol] += pos.trade_count

        if not symbol_pnl:
            print("No symbol data available.")
            return

        PerformanceFormatter.print_header("SYMBOL BREAKDOWN")
        print(f"{'Symbol':<15} {'Trades':>10} {'Realized PnL':>18} {'% of Total':>15}")
        PerformanceFormatter.print_separator("-", 70)

        total_pnl = sum(symbol_pnl.values())
        for symbol in sorted(symbol_pnl.keys()):
            pnl = symbol_pnl[symbol]
            trades = symbol_trades[symbol]
            pct_of_total = (pnl / total_pnl * 100) if total_pnl != 0 else Decimal("0")
            print(
                f"{symbol:<15} "
                f"{trades:>10} "
                f"{PerformanceFormatter.format_decimal(pnl):>18} "
                f"{PerformanceFormatter.format_pct(float(pct_of_total)):>15}"
            )

        PerformanceFormatter.print_separator("-", 70)
        print(f"{'TOTAL':<15} {'':>10} {PerformanceFormatter.format_decimal(total_pnl):>18} {'':>15}")
        print()

    @staticmethod
    def print_comparison(
        comparison: PerformanceComparison,
        ratio: float = 1.0,
        correct_live_net_profit: Optional[Decimal] = None,
        first_label: str = "First",
        second_label: str = "Second",
    ):
        print("\n" + "=" * 70)
        print("COMPARISON RESULTS")
        print("=" * 70)

        first = comparison.first
        second = comparison.second

        if correct_live_net_profit is not None:
            second = Performance(
                total_trades=second.total_trades,
                open_positions=second.open_positions,
                winning_trades=second.winning_trades,
                losing_trades=second.losing_trades,
                win_rate=second.win_rate,
                net_profit=correct_live_net_profit,
                net_profit_pct=second.net_profit_pct,
                max_drawdown=second.max_drawdown,
                sharpe_ratio=second.sharpe_ratio,
                final_value=second.final_value,
                initial_cash=second.initial_cash,
                total_commission=second.total_commission,
                max_single_win=second.max_single_win,
                max_single_loss=second.max_single_loss,
                max_single_win_pct=second.max_single_win_pct,
                max_single_loss_pct=second.max_single_loss_pct,
                avg_win=second.avg_win,
                avg_loss=second.avg_loss,
                avg_win_pct=second.avg_win_pct,
                avg_loss_pct=second.avg_loss_pct,
                odds_ratio=second.odds_ratio,
                total_win=second.total_win,
                total_loss=second.total_loss,
                commission_loss_pct=second.commission_loss_pct,
                sortino_ratio=second.sortino_ratio,
                calmar_ratio=second.calmar_ratio,
                top_1pct_win_pct=second.top_1pct_win_pct,
                top_5pct_win_pct=second.top_5pct_win_pct,
                top_10pct_win_pct=second.top_10pct_win_pct,
                top_20pct_win_pct=second.top_20pct_win_pct,
                top_1pct_loss_pct=second.top_1pct_loss_pct,
                top_5pct_loss_pct=second.top_5pct_loss_pct,
                top_10pct_loss_pct=second.top_10pct_loss_pct,
                top_20pct_loss_pct=second.top_20pct_loss_pct,
            )

        scaled_first = first.net_profit * Decimal(str(ratio))

        print(f"{'Metric':<35} {first_label:>18} {second_label:>18} {'Delta':>18}")
        print("-" * 70)
        print(f"{'Net Profit:':<35} {PerformanceFormatter.format_decimal(scaled_first):>18} {PerformanceFormatter.format_decimal(second.net_profit):>18} {PerformanceFormatter.format_decimal(second.net_profit - scaled_first):>18}")
        print(f"{'Net Profit %:':<35} {PerformanceFormatter.format_pct(first.net_profit_pct):>18} {PerformanceFormatter.format_pct(second.net_profit_pct):>18} {PerformanceFormatter.format_pct(second.net_profit_pct - first.net_profit_pct):>18}")
        print(f"{'Win Rate:':<35} {PerformanceFormatter.format_pct(first.win_rate):>18} {PerformanceFormatter.format_pct(second.win_rate):>18} {PerformanceFormatter.format_pct(second.win_rate - first.win_rate):>18}")
        print(f"{'Total Trades:':<35} {first.total_trades:>18} {second.total_trades:>18} {second.total_trades - first.total_trades:>18}")
        print(f"{'Max Drawdown:':<35} {PerformanceFormatter.format_decimal(first.max_drawdown):>18} {PerformanceFormatter.format_decimal(second.max_drawdown):>18} {PerformanceFormatter.format_decimal(second.max_drawdown - first.max_drawdown):>18}")
        print(f"{'Sharpe Ratio:':<35} {first.sharpe_ratio:>18.4f} {second.sharpe_ratio:>18.4f} {second.sharpe_ratio - first.sharpe_ratio:>18.4f}")
        print()

        print(f"{'Performance Ratio ({second_label}/{first_label}):':<35} {comparison.performance_ratio:>18.4f}")
        print(f"{'Drift %:':<35} {PerformanceFormatter.format_pct(comparison.drift_percentage):>18}")
        print(f"{'Total Sessions:':<35} {comparison.total_sessions:>18}")
        print(f"{'Matched Sessions:':<35} {comparison.matched_sessions:>18}")
        print(f"{'Match Rate:':<35} {PerformanceFormatter.format_pct(comparison.session_match_rate):>18}")
        print()
