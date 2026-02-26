"""Tests for PerformanceFormatter."""
from decimal import Decimal
import pytest
from io import StringIO
import sys
from evaluator.formatters.formatter import PerformanceFormatter
from evaluator.models.performance import Performance
from evaluator.models.session_stats import SessionStats
from evaluator.models.position_session_stats import PositionSessionStats
from evaluator.models.comparison import PerformanceComparison


class TestPerformanceFormatter:
    """Tests for PerformanceFormatter."""

    def test_format_decimal_default(self):
        """Test format_decimal with default decimals."""
        result = PerformanceFormatter.format_decimal(Decimal("1234.567"))
        assert result == "1,234.57"

    def test_format_decimal_custom_decimals(self):
        """Test format_decimal with custom decimals."""
        result = PerformanceFormatter.format_decimal(Decimal("1234.5678"), decimals=3)
        assert result == "1,234.568"

    def test_format_decimal_zero(self):
        """Test format_decimal with zero."""
        result = PerformanceFormatter.format_decimal(Decimal("0"))
        assert result == "0.00"

    def test_format_decimal_negative(self):
        """Test format_decimal with negative value."""
        result = PerformanceFormatter.format_decimal(Decimal("-1234.56"))
        assert result == "-1,234.56"

    def test_format_decimal_large_value(self):
        """Test format_decimal with large value."""
        result = PerformanceFormatter.format_decimal(Decimal("999999999.99"))
        assert result == "999,999,999.99"

    def test_format_decimal_small_value(self):
        """Test format_decimal with small value."""
        result = PerformanceFormatter.format_decimal(Decimal("0.001"))
        assert result == "0.00"

    def test_format_pct_default(self):
        """Test format_pct with default decimals."""
        result = PerformanceFormatter.format_pct(12.345)
        assert result == "12.35%"

    def test_format_pct_custom_decimals(self):
        """Test format_pct with custom decimals."""
        result = PerformanceFormatter.format_pct(12.3456, decimals=3)
        assert result == "12.346%"

    def test_format_pct_zero(self):
        """Test format_pct with zero."""
        result = PerformanceFormatter.format_pct(0.0)
        assert result == "0.00%"

    def test_format_pct_negative(self):
        """Test format_pct with negative value."""
        result = PerformanceFormatter.format_pct(-5.5)
        assert result == "-5.50%"

    def test_format_pct_large_value(self):
        """Test format_pct with large value."""
        result = PerformanceFormatter.format_pct(150.75)
        assert result == "150.75%"

    def test_calculate_base_amount_empty(self):
        """Test calculate_base_amount with empty sessions."""
        result = PerformanceFormatter.calculate_base_amount([])
        assert result == Decimal("0")

    def test_calculate_base_amount_single_session(self):
        """Test calculate_base_amount with single session."""
        sessions = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
            ),
        ]
        result = PerformanceFormatter.calculate_base_amount(sessions)
        assert result == Decimal("100000")

    def test_calculate_base_amount_multiple_sessions(self):
        """Test calculate_base_amount with multiple sessions."""
        sessions = [
            SessionStats(session=20251115, start_cash=Decimal("100000")),
            SessionStats(session=20251118, start_cash=Decimal("0")),
            SessionStats(session=20251119, start_cash=Decimal("0")),
        ]
        result = PerformanceFormatter.calculate_base_amount(sessions)
        assert result == Decimal("100000")

    def test_calculate_base_amount_first_zero(self):
        """Test calculate_base_amount when first session is zero."""
        sessions = [
            SessionStats(session=20251115, start_cash=Decimal("0")),
            SessionStats(session=20251118, start_cash=Decimal("100000")),
        ]
        result = PerformanceFormatter.calculate_base_amount(sessions)
        assert result == Decimal("100000")

    def test_calculate_base_amount_all_zero(self):
        """Test calculate_base_amount when all sessions are zero."""
        sessions = [
            SessionStats(session=20251115, start_cash=Decimal("0")),
            SessionStats(session=20251118, start_cash=Decimal("0")),
        ]
        result = PerformanceFormatter.calculate_base_amount(sessions)
        assert result == Decimal("0")

    def test_print_separator_default(self):
        """Test print_separator with defaults."""
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_separator()
        sys.stdout = sys.__stdout__
        assert len(captured.getvalue()) == 71  # 70 chars + newline

    def test_print_separator_custom_char(self):
        """Test print_separator with custom char."""
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_separator(char="-", length=50)
        sys.stdout = sys.__stdout__
        assert len(captured.getvalue()) == 51  # 50 chars + newline

    def test_print_header(self):
        """Test print_header."""
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_header("TEST TITLE")
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        assert "TEST TITLE" in output

    def test_print_performance_metrics_none(self):
        """Test print_performance_metrics with None."""
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_performance_metrics(None)
        sys.stdout = sys.__stdout__
        assert "No performance data" in captured.getvalue()

    def test_print_performance_metrics_with_data(self):
        """Test print_performance_metrics with valid data."""
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
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_performance_metrics(perf)
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        assert "Net Profit" in output

    def test_print_account_summary_empty(self):
        """Test print_account_summary with empty sessions."""
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_account_summary([])
        sys.stdout = sys.__stdout__
        assert "No session data" in captured.getvalue()

    def test_print_account_summary_with_data(self):
        """Test print_account_summary with valid data."""
        sessions = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
                end_cash=Decimal("110000"),
            ),
            SessionStats(
                session=20251118,
                start_cash=Decimal("110000"),
                end_cash=Decimal("120000"),
            ),
        ]
        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            PerformanceFormatter.print_account_summary(sessions)
        finally:
            sys.stdout = old_stdout
        output = captured.getvalue()
        assert "ACCOUNT SUMMARY" in output

    def test_print_session_details_empty(self):
        """Test print_session_details with empty sessions."""
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_session_details([])
        sys.stdout = sys.__stdout__
        assert "No session data" in captured.getvalue()

    def test_print_session_details_with_data(self):
        """Test print_session_details with valid data."""
        sessions = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
                end_cash=Decimal("110000"),
            ),
        ]
        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            PerformanceFormatter.print_session_details(sessions)
        finally:
            sys.stdout = old_stdout
        output = captured.getvalue()
        assert "SESSION DETAILS" in output

    def test_print_symbol_breakdown_empty(self):
        """Test print_symbol_breakdown with empty sessions."""
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_symbol_breakdown([])
        sys.stdout = sys.__stdout__
        assert "No session data" in captured.getvalue()

    def test_print_symbol_breakdown_with_data(self):
        """Test print_symbol_breakdown with valid data."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                realized_profit=Decimal("1000"),
                trade_count=2,
            ),
        ]
        sessions = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
                end_cash=Decimal("100000"),
                end_positions=positions,
            ),
        ]
        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            PerformanceFormatter.print_symbol_breakdown(sessions)
        finally:
            sys.stdout = old_stdout
        output = captured.getvalue()
        assert "SYMBOL BREAKDOWN" in output or "No symbol data" in output

    def test_print_comparison_basic(self):
        """Test print_comparison with basic data."""
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
        comparison = PerformanceComparison(
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
            matched_sessions=10,
            session_match_rate=1.0,
        )
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_comparison(comparison)
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        assert "COMPARISON RESULTS" in output

    def test_print_comparison_with_corrected_live(self):
        """Test print_comparison with corrected live net profit."""
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
        comparison = PerformanceComparison(
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
            matched_sessions=10,
            session_match_rate=1.0,
        )
        captured = StringIO()
        sys.stdout = captured
        PerformanceFormatter.print_comparison(comparison, correct_live_net_profit=Decimal("8500"))
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        assert "COMPARISON RESULTS" in output
