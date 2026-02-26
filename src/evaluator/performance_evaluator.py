import logging
from abc import ABC
from decimal import Decimal
from typing import List

from .models.performance import Performance
from .models.session_stats import SessionStats
from .models.comparison import PerformanceComparison, SessionComparison
from .calculators import PerformanceCalculator

logger = logging.getLogger(__name__)


class PerformanceEvaluator(ABC):
    def __init__(self, risk_free_rate: float = 0.03):
        self._risk_free_rate = risk_free_rate

    def evaluate(
        self,
        sessions: List[SessionStats]
    ) -> Performance:
        if not sessions:
            return self._empty_performance()

        return self._evaluate(sessions)

    def compare(
        self,
        sessions_a: List[SessionStats],
        sessions_b: List[SessionStats],
    ) -> PerformanceComparison:
        sessions_a_ids = set(s.session for s in sessions_a)
        sessions_b_ids = set(s.session for s in sessions_b)

        if sessions_a_ids != sessions_b_ids:
            only_in_a = sessions_a_ids - sessions_b_ids
            only_in_b = sessions_b_ids - sessions_a_ids

            if only_in_a:
                logger.warning(
                    f"Sessions only in first set: {sorted(only_in_a)}. "
                    f"Comparison will only use common sessions."
                )
            if only_in_b:
                logger.warning(
                    f"Sessions only in second set: {sorted(only_in_b)}. "
                    f"Comparison will only use common sessions."
                )

        perf_a = self.evaluate(sessions_a)
        perf_b = self.evaluate(sessions_b)

        session_comparisons = self._compare_sessions(sessions_a, sessions_b)

        all_sessions = sessions_a_ids | sessions_b_ids
        matched = len(sessions_a_ids & sessions_b_ids)

        first_net = perf_a.net_profit
        net_delta = perf_b.net_profit - perf_a.net_profit

        if first_net != Decimal("0"):
            perf_ratio = float(perf_b.net_profit / first_net)
            drift_pct = abs(float(net_delta / first_net) * 100)
        else:
            perf_ratio = 0.0
            drift_pct = 0.0

        return PerformanceComparison(
            first=perf_a,
            second=perf_b,
            net_profit_delta=net_delta,
            net_profit_pct_delta=perf_b.net_profit_pct - perf_a.net_profit_pct,
            win_rate_delta=perf_b.win_rate - perf_a.win_rate,
            sharpe_ratio_delta=perf_b.sharpe_ratio - perf_a.sharpe_ratio,
            max_drawdown_delta=perf_b.max_drawdown - perf_a.max_drawdown,
            total_trades_delta=perf_b.total_trades - perf_a.total_trades,
            performance_ratio=perf_ratio,
            drift_percentage=drift_pct,
            sessions=session_comparisons,
            total_sessions=len(all_sessions),
            matched_sessions=matched,
            session_match_rate=matched / len(all_sessions) if all_sessions else 0.0,
        )

    def _compare_sessions(
        self,
        first_sessions: List[SessionStats],
        second_sessions: List[SessionStats],
    ) -> List[SessionComparison]:
        first_by_session = {s.session: s for s in first_sessions}
        second_by_session = {s.session: s for s in second_sessions}

        common_sessions = set(first_by_session.keys()) & set(second_by_session.keys())

        comparisons = []
        for session in sorted(common_sessions):
            first = first_by_session[session]
            second = second_by_session[session]

            first_pnl = first.profit_loss
            second_pnl = second.profit_loss
            pnl_delta = second_pnl - first_pnl

            first_pnl_pct = float(first_pnl / first.start_cash * 100) if first.start_cash != 0 else 0.0
            second_pnl_pct = float(second_pnl / second.start_cash * 100) if second.start_cash != 0 else 0.0

            first_trade_count = len(first.end_positions)
            second_trade_count = len(second.end_positions)

            drift_ratio = float(pnl_delta / abs(first_pnl)) if first_pnl != 0 else 0.0

            comparisons.append(SessionComparison(
                session=session,
                first_pnl=first_pnl,
                first_pnl_pct=first_pnl_pct,
                first_trade_count=first_trade_count,
                first_end_cash=first.end_cash,
                second_pnl=second_pnl,
                second_pnl_pct=second_pnl_pct,
                second_trade_count=second_trade_count,
                second_end_cash=second.end_cash,
                pnl_delta=pnl_delta,
                pnl_pct_delta=second_pnl_pct - first_pnl_pct,
                trade_count_delta=second_trade_count - first_trade_count,
                drift_ratio=drift_ratio,
            ))

        return comparisons

    def _evaluate(
        self,
        sessions: List[SessionStats]
    ) -> Performance:
        return PerformanceCalculator.compute_account_performance(sessions, self._risk_free_rate)

    def _empty_performance(self) -> Performance:
        return PerformanceCalculator._empty_performance()

    def evaluate_position(
        self,
        position_stats: dict,
        symbol: str,
    ) -> Performance:
        if not position_stats:
            return self._empty_position_performance(symbol)
        return PerformanceCalculator.compute_position_performance(position_stats, symbol, self._risk_free_rate)

    def _empty_position_performance(self, symbol: str) -> Performance:
        return PerformanceCalculator._empty_position_performance(symbol)
