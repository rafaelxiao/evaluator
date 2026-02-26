"""Tests for PerformanceComparison and SessionComparison models."""
from decimal import Decimal
import pytest
from evaluator.models.comparison import PerformanceComparison, SessionComparison
from evaluator.models.performance import Performance


class TestSessionComparison:
    """Tests for SessionComparison model."""

    def test_session_comparison_full_init(self):
        """Test creating SessionComparison with all fields."""
        comp = SessionComparison(
            session=20251115,
            first_pnl=Decimal("1000"),
            first_pnl_pct=10.0,
            first_trade_count=5,
            first_end_cash=Decimal("110000"),
            second_pnl=Decimal("800"),
            second_pnl_pct=8.0,
            second_trade_count=4,
            second_end_cash=Decimal("108000"),
            pnl_delta=Decimal("-200"),
            pnl_pct_delta=-2.0,
            trade_count_delta=-1,
            drift_ratio=0.2,
        )
        assert comp.session == 20251115
        assert comp.first_pnl == Decimal("1000")
        assert comp.second_pnl == Decimal("800")
        assert comp.pnl_delta == Decimal("-200")
        assert comp.drift_ratio == 0.2

    def test_session_comparison_minimal_init(self):
        """Test creating SessionComparison with minimal fields."""
        comp = SessionComparison(
            session=20251115,
            first_pnl=Decimal("1000"),
            first_pnl_pct=10.0,
            first_trade_count=5,
            first_end_cash=Decimal("110000"),
            second_pnl=Decimal("1000"),
            second_pnl_pct=10.0,
            second_trade_count=5,
            second_end_cash=Decimal("110000"),
            pnl_delta=Decimal("0"),
            pnl_pct_delta=0.0,
            trade_count_delta=0,
            drift_ratio=0.0,
        )
        assert comp.session == 20251115

    def test_session_comparison_positive_delta(self):
        """Test SessionComparison with positive delta (second > first)."""
        comp = SessionComparison(
            session=20251115,
            first_pnl=Decimal("1000"),
            first_pnl_pct=10.0,
            first_trade_count=5,
            first_end_cash=Decimal("110000"),
            second_pnl=Decimal("1500"),
            second_pnl_pct=15.0,
            second_trade_count=6,
            second_end_cash=Decimal("115000"),
            pnl_delta=Decimal("500"),
            pnl_pct_delta=5.0,
            trade_count_delta=1,
            drift_ratio=0.5,
        )
        assert comp.pnl_delta > 0

    def test_session_comparison_negative_delta(self):
        """Test SessionComparison with negative delta."""
        comp = SessionComparison(
            session=20251115,
            first_pnl=Decimal("1000"),
            first_pnl_pct=10.0,
            first_trade_count=5,
            first_end_cash=Decimal("110000"),
            second_pnl=Decimal("500"),
            second_pnl_pct=5.0,
            second_trade_count=3,
            second_end_cash=Decimal("105000"),
            pnl_delta=Decimal("-500"),
            pnl_pct_delta=-5.0,
            trade_count_delta=-2,
            drift_ratio=0.5,
        )
        assert comp.pnl_delta < 0

    def test_session_comparison_zero_drift(self):
        """Test SessionComparison with zero drift."""
        comp = SessionComparison(
            session=20251115,
            first_pnl=Decimal("0"),
            first_pnl_pct=0.0,
            first_trade_count=5,
            first_end_cash=Decimal("100000"),
            second_pnl=Decimal("0"),
            second_pnl_pct=0.0,
            second_trade_count=5,
            second_end_cash=Decimal("100000"),
            pnl_delta=Decimal("0"),
            pnl_pct_delta=0.0,
            trade_count_delta=0,
            drift_ratio=0.0,
        )
        assert comp.drift_ratio == 0.0

    def test_session_comparison_large_values(self):
        """Test SessionComparison with large values."""
        comp = SessionComparison(
            session=20251115,
            first_pnl=Decimal("999999999.99"),
            first_pnl_pct=999.99,
            first_trade_count=10000,
            first_end_cash=Decimal("9999999999"),
            second_pnl=Decimal("888888888.88"),
            second_pnl_pct=888.88,
            second_trade_count=9000,
            second_end_cash=Decimal("8888888888"),
            pnl_delta=Decimal("-111111111.11"),
            pnl_pct_delta=-111.11,
            trade_count_delta=-1000,
            drift_ratio=0.111,
        )
        assert comp.first_pnl == Decimal("999999999.99")

    def test_session_comparison_negative_pnl(self):
        """Test SessionComparison with negative pnl."""
        comp = SessionComparison(
            session=20251115,
            first_pnl=Decimal("-500"),
            first_pnl_pct=-5.0,
            first_trade_count=5,
            first_end_cash=Decimal("95000"),
            second_pnl=Decimal("-300"),
            second_pnl_pct=-3.0,
            second_trade_count=4,
            second_end_cash=Decimal("97000"),
            pnl_delta=Decimal("200"),
            pnl_pct_delta=2.0,
            trade_count_delta=-1,
            drift_ratio=0.4,
        )
        assert comp.first_pnl < 0


class TestPerformanceComparison:
    """Tests for PerformanceComparison model."""

    def test_performance_comparison_full_init(self):
        """Test creating PerformanceComparison with all fields."""
        perf1 = Performance(
            total_trades=10,
            winning_trades=6,
            losing_trades=4,
            win_rate=60.0,
            net_profit=Decimal("10000"),
            net_profit_pct=20.0,
            max_drawdown=Decimal("2000"),
            sharpe_ratio=1.5,
            final_value=Decimal("60000"),
            initial_cash=Decimal("50000"),
        )
        perf2 = Performance(
            total_trades=8,
            winning_trades=5,
            losing_trades=3,
            win_rate=62.5,
            net_profit=Decimal("8000"),
            net_profit_pct=16.0,
            max_drawdown=Decimal("2500"),
            sharpe_ratio=1.2,
            final_value=Decimal("58000"),
            initial_cash=Decimal("50000"),
        )
        comp = PerformanceComparison(
            first=perf1,
            second=perf2,
            net_profit_delta=Decimal("-2000"),
            net_profit_pct_delta=-4.0,
            win_rate_delta=2.5,
            sharpe_ratio_delta=-0.3,
            max_drawdown_delta=Decimal("500"),
            total_trades_delta=-2,
            performance_ratio=0.8,
            drift_percentage=20.0,
            sessions=[],
            total_sessions=10,
            matched_sessions=8,
            session_match_rate=0.8,
        )
        assert comp.first.net_profit == Decimal("10000")
        assert comp.second.net_profit == Decimal("8000")
        assert comp.net_profit_delta == Decimal("-2000")
        assert comp.performance_ratio == 0.8

    def test_performance_comparison_minimal_init(self):
        """Test creating PerformanceComparison with minimal fields."""
        perf1 = Performance(
            total_trades=10,
            winning_trades=6,
            losing_trades=4,
            win_rate=60.0,
            net_profit=Decimal("10000"),
            net_profit_pct=20.0,
            max_drawdown=Decimal("2000"),
            sharpe_ratio=1.5,
            final_value=Decimal("60000"),
            initial_cash=Decimal("50000"),
        )
        perf2 = Performance(
            total_trades=10,
            winning_trades=6,
            losing_trades=4,
            win_rate=60.0,
            net_profit=Decimal("10000"),
            net_profit_pct=20.0,
            max_drawdown=Decimal("2000"),
            sharpe_ratio=1.5,
            final_value=Decimal("60000"),
            initial_cash=Decimal("50000"),
        )
        comp = PerformanceComparison(
            first=perf1,
            second=perf2,
            net_profit_delta=Decimal("0"),
            net_profit_pct_delta=0.0,
            win_rate_delta=0.0,
            sharpe_ratio_delta=0.0,
            max_drawdown_delta=Decimal("0"),
            total_trades_delta=0,
            performance_ratio=1.0,
            drift_percentage=0.0,
            total_sessions=10,
            matched_sessions=10,
            session_match_rate=1.0,
        )
        assert comp.drift_percentage == 0.0

    def test_performance_comparison_with_sessions(self):
        """Test PerformanceComparison with session comparisons."""
        perf1 = Performance(
            total_trades=10,
            winning_trades=6,
            losing_trades=4,
            win_rate=60.0,
            net_profit=Decimal("10000"),
            net_profit_pct=20.0,
            max_drawdown=Decimal("2000"),
            sharpe_ratio=1.5,
            final_value=Decimal("60000"),
            initial_cash=Decimal("50000"),
        )
        perf2 = Performance(
            total_trades=8,
            winning_trades=5,
            losing_trades=3,
            win_rate=62.5,
            net_profit=Decimal("8000"),
            net_profit_pct=16.0,
            max_drawdown=Decimal("2500"),
            sharpe_ratio=1.2,
            final_value=Decimal("58000"),
            initial_cash=Decimal("50000"),
        )
        sessions = [
            SessionComparison(
                session=20251115,
                first_pnl=Decimal("1000"),
                first_pnl_pct=10.0,
                first_trade_count=5,
                first_end_cash=Decimal("110000"),
                second_pnl=Decimal("800"),
                second_pnl_pct=8.0,
                second_trade_count=4,
                second_end_cash=Decimal("108000"),
                pnl_delta=Decimal("-200"),
                pnl_pct_delta=-2.0,
                trade_count_delta=-1,
                drift_ratio=0.2,
            ),
            SessionComparison(
                session=20251118,
                first_pnl=Decimal("1500"),
                first_pnl_pct=15.0,
                first_trade_count=6,
                first_end_cash=Decimal("111500"),
                second_pnl=Decimal("1200"),
                second_pnl_pct=12.0,
                second_trade_count=5,
                second_end_cash=Decimal("111200"),
                pnl_delta=Decimal("-300"),
                pnl_pct_delta=-3.0,
                trade_count_delta=-1,
                drift_ratio=0.2,
            ),
        ]
        comp = PerformanceComparison(
            first=perf1,
            second=perf2,
            net_profit_delta=Decimal("-2000"),
            net_profit_pct_delta=-4.0,
            win_rate_delta=2.5,
            sharpe_ratio_delta=-0.3,
            max_drawdown_delta=Decimal("500"),
            total_trades_delta=-2,
            performance_ratio=0.8,
            drift_percentage=20.0,
            sessions=sessions,
            total_sessions=10,
            matched_sessions=2,
            session_match_rate=0.2,
        )
        assert len(comp.sessions) == 2
        assert comp.sessions[0].session == 20251115
        assert comp.sessions[1].session == 20251118

    def test_performance_comparison_perfect_match(self):
        """Test PerformanceComparison with identical performances."""
        perf = Performance(
            total_trades=10,
            winning_trades=6,
            losing_trades=4,
            win_rate=60.0,
            net_profit=Decimal("10000"),
            net_profit_pct=20.0,
            max_drawdown=Decimal("2000"),
            sharpe_ratio=1.5,
            final_value=Decimal("60000"),
            initial_cash=Decimal("50000"),
        )
        comp = PerformanceComparison(
            first=perf,
            second=perf,
            net_profit_delta=Decimal("0"),
            net_profit_pct_delta=0.0,
            win_rate_delta=0.0,
            sharpe_ratio_delta=0.0,
            max_drawdown_delta=Decimal("0"),
            total_trades_delta=0,
            performance_ratio=1.0,
            drift_percentage=0.0,
            total_sessions=10,
            matched_sessions=10,
            session_match_rate=1.0,
        )
        assert comp.performance_ratio == 1.0
        assert comp.drift_percentage == 0.0

    def test_performance_comparison_second_better(self):
        """Test PerformanceComparison where second outperforms first."""
        perf1 = Performance(
            total_trades=10,
            winning_trades=5,
            losing_trades=5,
            win_rate=50.0,
            net_profit=Decimal("5000"),
            net_profit_pct=10.0,
            max_drawdown=Decimal("3000"),
            sharpe_ratio=1.0,
            final_value=Decimal("55000"),
            initial_cash=Decimal("50000"),
        )
        perf2 = Performance(
            total_trades=12,
            winning_trades=8,
            losing_trades=4,
            win_rate=66.67,
            net_profit=Decimal("12000"),
            net_profit_pct=24.0,
            max_drawdown=Decimal("2000"),
            sharpe_ratio=2.0,
            final_value=Decimal("62000"),
            initial_cash=Decimal("50000"),
        )
        comp = PerformanceComparison(
            first=perf1,
            second=perf2,
            net_profit_delta=Decimal("7000"),
            net_profit_pct_delta=14.0,
            win_rate_delta=16.67,
            sharpe_ratio_delta=1.0,
            max_drawdown_delta=Decimal("-1000"),
            total_trades_delta=2,
            performance_ratio=2.4,
            drift_percentage=140.0,
            total_sessions=10,
            matched_sessions=10,
            session_match_rate=1.0,
        )
        assert comp.net_profit_delta > 0
        assert comp.performance_ratio > 1.0

    def test_performance_comparison_large_negative_delta(self):
        """Test PerformanceComparison with large negative delta."""
        perf1 = Performance(
            total_trades=100,
            winning_trades=80,
            losing_trades=20,
            win_rate=80.0,
            net_profit=Decimal("100000"),
            net_profit_pct=100.0,
            max_drawdown=Decimal("5000"),
            sharpe_ratio=3.0,
            final_value=Decimal("200000"),
            initial_cash=Decimal("100000"),
        )
        perf2 = Performance(
            total_trades=10,
            winning_trades=1,
            losing_trades=9,
            win_rate=10.0,
            net_profit=Decimal("-50000"),
            net_profit_pct=-50.0,
            max_drawdown=Decimal("80000"),
            sharpe_ratio=-0.5,
            final_value=Decimal("50000"),
            initial_cash=Decimal("100000"),
        )
        comp = PerformanceComparison(
            first=perf1,
            second=perf2,
            net_profit_delta=Decimal("-150000"),
            net_profit_pct_delta=-150.0,
            win_rate_delta=-70.0,
            sharpe_ratio_delta=-3.5,
            max_drawdown_delta=Decimal("75000"),
            total_trades_delta=-90,
            performance_ratio=-0.5,
            drift_percentage=150.0,
            total_sessions=10,
            matched_sessions=5,
            session_match_rate=0.5,
        )
        assert comp.net_profit_delta < 0

    def test_performance_comparison_zero_match_rate(self):
        """Test PerformanceComparison with zero match rate."""
        perf1 = Performance(
            total_trades=10,
            winning_trades=6,
            losing_trades=4,
            win_rate=60.0,
            net_profit=Decimal("10000"),
            net_profit_pct=20.0,
            max_drawdown=Decimal("2000"),
            sharpe_ratio=1.5,
            final_value=Decimal("60000"),
            initial_cash=Decimal("50000"),
        )
        perf2 = Performance(
            total_trades=8,
            winning_trades=5,
            losing_trades=3,
            win_rate=62.5,
            net_profit=Decimal("8000"),
            net_profit_pct=16.0,
            max_drawdown=Decimal("2500"),
            sharpe_ratio=1.2,
            final_value=Decimal("58000"),
            initial_cash=Decimal("50000"),
        )
        comp = PerformanceComparison(
            first=perf1,
            second=perf2,
            net_profit_delta=Decimal("-2000"),
            net_profit_pct_delta=-4.0,
            win_rate_delta=2.5,
            sharpe_ratio_delta=-0.3,
            max_drawdown_delta=Decimal("500"),
            total_trades_delta=-2,
            performance_ratio=0.8,
            drift_percentage=20.0,
            total_sessions=10,
            matched_sessions=0,
            session_match_rate=0.0,
        )
        assert comp.session_match_rate == 0.0
