from decimal import Decimal
from typing import List

from ..models.performance import Performance
from ..models.session_stats import SessionStats
from ..models.position_session_stats import PositionSessionStats
from .ratio import RatioCalculator


class PerformanceCalculator:
    """绩效计算器 - 计算账户和持仓绩效"""

    @staticmethod
    def compute_account_performance(
        session_stats: List[SessionStats],
        risk_free_rate: float,
    ) -> Performance:
        """计算账户绩效"""
        if not session_stats:
            return PerformanceCalculator._empty_account_performance()

        base_amount = Decimal("0")
        for s in session_stats:
            if s.start_cash > 0:
                base_amount = s.start_cash
                break

        initial_cash = session_stats[0].end_cash
        final_value = session_stats[-1].end_market_value
        total_commission = sum(s.total_commission for s in session_stats)

        equity_curve = []
        peak = initial_cash
        max_drawdown = Decimal("0")

        session_pnls = []
        for s in session_stats:
            equity = s.end_market_value
            equity_curve.append(float(equity))
            if equity > peak:
                peak = equity
            drawdown = peak - equity
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        winning_trades = 0
        losing_trades = 0
        total_win = Decimal("0")
        total_loss = Decimal("0")
        max_single_win = Decimal("0")
        max_single_loss = Decimal("0")
        wins = []
        losses = []

        first_session = True
        for s in session_stats:
            pnl = s.profit_loss

            if first_session:
                pnl = pnl - base_amount + s.start_cash
                first_session = False

            session_pnls.append(float(pnl))

            if pnl > 0:
                winning_trades += 1
                total_win += pnl
                wins.append(float(pnl))
                if pnl > max_single_win:
                    max_single_win = pnl
            elif pnl < 0:
                losing_trades += 1
                total_loss += pnl
                losses.append(float(pnl))
                if pnl < max_single_loss:
                    max_single_loss = pnl

        total_trades = winning_trades + losing_trades
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        net_profit = final_value - initial_cash
        net_profit_pct = float(net_profit / initial_cash * 100) if initial_cash != 0 else 0.0

        avg_win = total_win / winning_trades if winning_trades > 0 else Decimal("0")
        avg_loss = total_loss / losing_trades if losing_trades > 0 else Decimal("0")
        avg_win_pct = float(avg_win / initial_cash * 100) if initial_cash != 0 else 0.0
        avg_loss_pct = float(avg_loss / initial_cash * 100) if initial_cash != 0 else 0.0
        odds_ratio = float(avg_win / avg_loss) if avg_loss != 0 else 0.0

        max_single_win_pct = float(max_single_win / initial_cash * 100) if initial_cash != 0 else 0.0
        max_single_loss_pct = float(max_single_loss / initial_cash * 100) if initial_cash != 0 else 0.0

        total_loss_val = abs(total_loss)
        commission_loss_pct = float(total_commission / total_loss_val * 100) if total_loss_val > 0 else 0.0

        total_win_amount = float(total_win) if total_win > 0 else 0.0
        total_loss_amount = float(abs(total_loss)) if total_loss < 0 else 0.0
        top_win_contributions = PerformanceCalculator._calculate_top_contributions(wins, total_win_amount)
        top_loss_contributions = PerformanceCalculator._calculate_top_contributions(losses, total_loss_amount, is_loss=True)

        sharpe_ratio = RatioCalculator.compute_sharpe_ratio(session_pnls, risk_free_rate, len(session_stats))
        sortino_ratio = RatioCalculator.compute_sortino_ratio(session_pnls, risk_free_rate, len(session_stats))
        calmar_ratio = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)

        return Performance(
            total_trades=total_trades,
            open_positions=len(session_stats[-1].end_positions),
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            net_profit=net_profit,
            net_profit_pct=net_profit_pct,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            final_value=final_value,
            initial_cash=initial_cash,
            total_commission=total_commission,
            max_single_win=max_single_win,
            max_single_loss=max_single_loss,
            max_single_win_pct=max_single_win_pct,
            max_single_loss_pct=max_single_loss_pct,
            avg_win=avg_win,
            avg_loss=avg_loss,
            avg_win_pct=avg_win_pct,
            avg_loss_pct=avg_loss_pct,
            odds_ratio=odds_ratio,
            total_win=total_win,
            total_loss=total_loss,
            commission_loss_pct=commission_loss_pct,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            top_1pct_win_pct=top_win_contributions[0],
            top_5pct_win_pct=top_win_contributions[1],
            top_10pct_win_pct=top_win_contributions[2],
            top_20pct_win_pct=top_win_contributions[3],
            top_1pct_loss_pct=top_loss_contributions[0],
            top_5pct_loss_pct=top_loss_contributions[1],
            top_10pct_loss_pct=top_loss_contributions[2],
            top_20pct_loss_pct=top_loss_contributions[3],
        )

    @staticmethod
    def _calculate_top_contributions(values: List[float], total: float, is_loss: bool = False) -> List[float]:
        if not values or total == 0:
            return [0.0, 0.0, 0.0, 0.0]

        if is_loss:
            sorted_values = sorted(values, reverse=False)
        else:
            sorted_values = sorted(values, reverse=True)

        def calc_contribution_pct(n_pct: float) -> float:
            n = max(1, int(len(sorted_values) * n_pct / 100))
            top_n_sum = sum(sorted_values[:n])
            if is_loss:
                top_n_sum = abs(top_n_sum)
            return (top_n_sum / total * 100) if total != 0 else 0.0

        return [
            calc_contribution_pct(1),
            calc_contribution_pct(5),
            calc_contribution_pct(10),
            calc_contribution_pct(20),
        ]

    @staticmethod
    def compute_position_performance(
        position_stats: dict,
        symbol: str,
        risk_free_rate: float,
    ) -> Performance:
        if not position_stats:
            return PerformanceCalculator._empty_position_performance(symbol)

        sessions = sorted(position_stats.keys())

        initial_cash = Decimal("0")
        final_value = Decimal("0")
        total_commission = Decimal("0")

        session_pnls = []
        equity_curve = []
        peak = Decimal("0")
        max_drawdown = Decimal("0")

        winning_trades = 0
        losing_trades = 0
        total_win = Decimal("0")
        total_loss = Decimal("0")
        max_single_win = Decimal("0")
        max_single_loss = Decimal("0")

        prev_end_value = Decimal("0")

        for session in sessions:
            data = position_stats[session]
            end_positions = data["end_positions"]

            if not end_positions:
                continue

            pos = end_positions[0]
            end_value = pos.end_value

            pnl = pos.profit_loss
            session_pnls.append(float(pnl))

            equity_curve.append(float(end_value))
            if end_value > peak:
                peak = end_value
            drawdown = peak - end_value
            if drawdown > max_drawdown:
                max_drawdown = drawdown

            if initial_cash == Decimal("0"):
                initial_cash = pos.start_value

            final_value = end_value
            total_commission += pos.commission

            if pnl > 0:
                winning_trades += 1
                total_win += pnl
                if pnl > max_single_win:
                    max_single_win = pnl
            elif pnl < 0:
                losing_trades += 1
                total_loss += pnl
                if pnl < max_single_loss:
                    max_single_loss = pnl

        total_trades = winning_trades + losing_trades
        if total_trades == 0:
            return PerformanceCalculator._empty_position_performance(symbol)

        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        net_profit = final_value - initial_cash
        net_profit_pct = float(net_profit / initial_cash * 100) if initial_cash != 0 else 0.0

        avg_win = total_win / winning_trades if winning_trades > 0 else Decimal("0")
        avg_loss = total_loss / losing_trades if losing_trades > 0 else Decimal("0")
        avg_win_pct = float(avg_win / initial_cash * 100) if initial_cash != 0 else 0.0
        avg_loss_pct = float(avg_loss / initial_cash * 100) if initial_cash != 0 else 0.0
        odds_ratio = float(avg_win / avg_loss) if avg_loss != 0 else 0.0

        max_single_win_pct = float(max_single_win / initial_cash * 100) if initial_cash != 0 else 0.0
        max_single_loss_pct = float(max_single_loss / initial_cash * 100) if initial_cash != 0 else 0.0

        total_loss_val = abs(total_loss)
        commission_loss_pct = float(total_commission / total_loss_val * 100) if total_loss_val > 0 else 0.0

        sharpe_ratio = RatioCalculator.compute_sharpe_ratio(session_pnls, risk_free_rate, len(sessions))
        sortino_ratio = RatioCalculator.compute_sortino_ratio(session_pnls, risk_free_rate, len(sessions))
        calmar_ratio = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)

        return Performance(
            symbol=symbol,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            net_profit=net_profit,
            net_profit_pct=net_profit_pct,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            final_value=final_value,
            initial_cash=initial_cash,
            total_commission=total_commission,
            max_single_win=max_single_win,
            max_single_loss=max_single_loss,
            max_single_win_pct=max_single_win_pct,
            max_single_loss_pct=max_single_loss_pct,
            avg_win=avg_win,
            avg_loss=avg_loss,
            avg_win_pct=avg_win_pct,
            avg_loss_pct=avg_loss_pct,
            odds_ratio=odds_ratio,
            total_win=total_win,
            total_loss=total_loss,
            commission_loss_pct=commission_loss_pct,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
        )

    @staticmethod
    def _empty_account_performance() -> Performance:
        return Performance(
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
            net_profit=Decimal("0"),
            net_profit_pct=0.0,
            max_drawdown=Decimal("0"),
            sharpe_ratio=0.0,
            final_value=Decimal("0"),
            initial_cash=Decimal("0"),
        )

    @staticmethod
    def _empty_performance() -> Performance:
        return Performance(
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
            net_profit=Decimal("0"),
            net_profit_pct=0.0,
            max_drawdown=Decimal("0"),
            sharpe_ratio=0.0,
            final_value=Decimal("0"),
            initial_cash=Decimal("0"),
        )

    @staticmethod
    def _empty_position_performance(symbol: str) -> Performance:
        return Performance(
            symbol=symbol,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
            net_profit=Decimal("0"),
            net_profit_pct=0.0,
            max_drawdown=Decimal("0"),
            sharpe_ratio=0.0,
            final_value=Decimal("0"),
            initial_cash=Decimal("0"),
        )
