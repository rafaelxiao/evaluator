"""Tests for Performance model."""
from decimal import Decimal
import pytest
from evaluator.models.performance import Performance


class TestPerformance:
    """Tests for Performance model."""

    def test_performance_full_init(self):
        """Test creating a Performance with all fields."""
        perf = Performance(
            total_trades=10,
            open_positions=2,
            winning_trades=6,
            losing_trades=4,
            win_rate=60.0,
            net_profit=Decimal("10000"),
            net_profit_pct=20.0,
            max_drawdown=Decimal("2000"),
            sharpe_ratio=1.5,
            final_value=Decimal("60000"),
            initial_cash=Decimal("50000"),
            total_commission=Decimal("100"),
            max_single_win=Decimal("3000"),
            max_single_loss=Decimal("1000"),
            max_single_win_pct=6.0,
            max_single_loss_pct=2.0,
            avg_win=Decimal("1666.67"),
            avg_loss=Decimal("500"),
            avg_win_pct=3.33,
            avg_loss_pct=1.0,
            odds_ratio=3.33,
            total_win=Decimal("10000"),
            total_loss=Decimal("2000"),
            max_drawdown_duration_bars=50,
            commission_loss_pct=1.0,
            top_1pct_win_pct=50.0,
            top_5pct_win_pct=70.0,
            top_10pct_win_pct=85.0,
            top_20pct_win_pct=95.0,
            top_1pct_loss_pct=30.0,
            top_5pct_loss_pct=50.0,
            top_10pct_loss_pct=70.0,
            top_20pct_loss_pct=90.0,
            sortino_ratio=2.0,
            calmar_ratio=5.0,
        )
        assert perf.total_trades == 10
        assert perf.open_positions == 2
        assert perf.winning_trades == 6
        assert perf.losing_trades == 4
        assert perf.win_rate == 60.0
        assert perf.net_profit == Decimal("10000")
        assert perf.net_profit_pct == 20.0
        assert perf.max_drawdown == Decimal("2000")
        assert perf.sharpe_ratio == 1.5
        assert perf.final_value == Decimal("60000")
        assert perf.initial_cash == Decimal("50000")
        assert perf.total_commission == Decimal("100")

    def test_performance_minimal_init(self):
        """Test creating a Performance with only required fields."""
        perf = Performance(
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
        assert perf.total_trades == 0
        assert perf.total_commission == Decimal("0")
        assert perf.max_single_win == Decimal("0")
        assert perf.max_single_loss == Decimal("0")
        assert perf.sortino_ratio == 0.0
        assert perf.calmar_ratio == 0.0

    def test_performance_defaults(self):
        """Test that default values are applied correctly."""
        perf = Performance(
            total_trades=5,
            winning_trades=3,
            losing_trades=2,
            win_rate=60.0,
            net_profit=Decimal("1000"),
            net_profit_pct=10.0,
            max_drawdown=Decimal("500"),
            sharpe_ratio=1.0,
            final_value=Decimal("11000"),
            initial_cash=Decimal("10000"),
        )
        assert perf.open_positions == 0
        assert perf.total_commission == Decimal("0")
        assert perf.max_single_win == Decimal("0")
        assert perf.max_single_loss == Decimal("0")
        assert perf.max_single_win_pct == 0.0
        assert perf.max_single_loss_pct == 0.0
        assert perf.avg_win == Decimal("0")
        assert perf.avg_loss == Decimal("0")
        assert perf.avg_win_pct == 0.0
        assert perf.avg_loss_pct == 0.0
        assert perf.odds_ratio == 0.0
        assert perf.total_win == Decimal("0")
        assert perf.total_loss == Decimal("0")
        assert perf.max_drawdown_duration_bars == 0
        assert perf.commission_loss_pct == 0.0
        assert perf.top_1pct_win_pct == 0.0
        assert perf.top_5pct_win_pct == 0.0
        assert perf.top_10pct_win_pct == 0.0
        assert perf.top_20pct_win_pct == 0.0
        assert perf.top_1pct_loss_pct == 0.0
        assert perf.top_5pct_loss_pct == 0.0
        assert perf.top_10pct_loss_pct == 0.0
        assert perf.top_20pct_loss_pct == 0.0
        assert perf.sortino_ratio == 0.0
        assert perf.calmar_ratio == 0.0

    def test_performance_frozen(self):
        """Test that Performance is not frozen (allows mutation)."""
        perf = Performance(
            total_trades=10,
            winning_trades=6,
            losing_trades=4,
            win_rate=60.0,
            net_profit=Decimal("1000"),
            net_profit_pct=10.0,
            max_drawdown=Decimal("500"),
            sharpe_ratio=1.0,
            final_value=Decimal("11000"),
            initial_cash=Decimal("10000"),
        )
        perf.total_trades = 20
        assert perf.total_trades == 20

    def test_performance_model_validation(self):
        """Test Performance model validation."""
        perf = Performance(
            total_trades=-1,  # Invalid
            winning_trades=6,
            losing_trades=4,
            win_rate=150.0,  # Invalid > 100
            net_profit=Decimal("1000"),
            net_profit_pct=10.0,
            max_drawdown=Decimal("500"),
            sharpe_ratio=1.0,
            final_value=Decimal("11000"),
            initial_cash=Decimal("10000"),
        )
        assert perf.total_trades == -1  # Pydantic doesn't validate by default

    def test_performance_with_large_values(self):
        """Test Performance with very large values."""
        perf = Performance(
            total_trades=1_000_000,
            open_positions=500_000,
            winning_trades=600_000,
            losing_trades=400_000,
            win_rate=60.0,
            net_profit=Decimal("999999999999.99"),
            net_profit_pct=999999.0,
            max_drawdown=Decimal("999999999"),
            sharpe_ratio=999.999,
            final_value=Decimal("9999999999999"),
            initial_cash=Decimal("1000000"),
            total_commission=Decimal("9999999.99"),
            max_single_win=Decimal("999999999"),
            max_single_loss=Decimal("999999999"),
            max_single_win_pct=999.0,
            max_single_loss_pct=999.0,
            avg_win=Decimal("1666666.67"),
            avg_loss=Decimal("250000"),
            avg_win_pct=166.67,
            avg_loss_pct=25.0,
            odds_ratio=6.67,
            total_win=Decimal("999999999"),
            total_loss=Decimal("99999999"),
            max_drawdown_duration_bars=999999,
            commission_loss_pct=99.99,
            top_1pct_win_pct=100.0,
            top_5pct_win_pct=100.0,
            top_10pct_win_pct=100.0,
            top_20pct_win_pct=100.0,
            top_1pct_loss_pct=100.0,
            top_5pct_loss_pct=100.0,
            top_10pct_loss_pct=100.0,
            top_20pct_loss_pct=100.0,
            sortino_ratio=999.999,
            calmar_ratio=999.999,
        )
        assert perf.total_trades == 1_000_000
        assert perf.net_profit == Decimal("999999999999.99")

    def test_performance_with_negative_values(self):
        """Test Performance with negative values."""
        perf = Performance(
            total_trades=10,
            open_positions=3,
            winning_trades=3,
            losing_trades=7,
            win_rate=30.0,
            net_profit=Decimal("-5000"),
            net_profit_pct=-10.0,
            max_drawdown=Decimal("8000"),
            sharpe_ratio=-0.5,
            final_value=Decimal("45000"),
            initial_cash=Decimal("50000"),
            total_commission=Decimal("200"),
            max_single_win=Decimal("500"),
            max_single_loss=Decimal("-3000"),
            max_single_win_pct=1.0,
            max_single_loss_pct=-6.0,
            avg_win=Decimal("166.67"),
            avg_loss=Decimal("-714.29"),
            avg_win_pct=0.33,
            avg_loss_pct=-1.43,
            odds_ratio=0.23,
            total_win=Decimal("500"),
            total_loss=Decimal("-5000"),
            max_drawdown_duration_bars=100,
            commission_loss_pct=2.0,
            top_1pct_win_pct=80.0,
            top_5pct_win_pct=90.0,
            top_10pct_win_pct=95.0,
            top_20pct_win_pct=100.0,
            top_1pct_loss_pct=20.0,
            top_5pct_loss_pct=40.0,
            top_10pct_loss_pct=60.0,
            top_20pct_loss_pct=80.0,
            sortino_ratio=-0.3,
            calmar_ratio=-0.625,
        )
        assert perf.net_profit < 0
        assert perf.max_drawdown > 0

    def test_performance_zero_values(self):
        """Test Performance with all zero values."""
        perf = Performance(
            total_trades=0,
            open_positions=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
            net_profit=Decimal("0"),
            net_profit_pct=0.0,
            max_drawdown=Decimal("0"),
            sharpe_ratio=0.0,
            final_value=Decimal("0"),
            initial_cash=Decimal("0"),
            total_commission=Decimal("0"),
            max_single_win=Decimal("0"),
            max_single_loss=Decimal("0"),
            max_single_win_pct=0.0,
            max_single_loss_pct=0.0,
            avg_win=Decimal("0"),
            avg_loss=Decimal("0"),
            avg_win_pct=0.0,
            avg_loss_pct=0.0,
            odds_ratio=0.0,
            total_win=Decimal("0"),
            total_loss=Decimal("0"),
            max_drawdown_duration_bars=0,
            commission_loss_pct=0.0,
            top_1pct_win_pct=0.0,
            top_5pct_win_pct=0.0,
            top_10pct_win_pct=0.0,
            top_20pct_win_pct=0.0,
            top_1pct_loss_pct=0.0,
            top_5pct_loss_pct=0.0,
            top_10pct_loss_pct=0.0,
            top_20pct_loss_pct=0.0,
            sortino_ratio=0.0,
            calmar_ratio=0.0,
        )
        assert perf.total_trades == 0
        assert perf.net_profit == Decimal("0")
        assert perf.sharpe_ratio == 0.0
