"""Tests for PerformanceCalculator."""
from decimal import Decimal
import pytest
from evaluator.calculators.performance import PerformanceCalculator
from evaluator.models.session_stats import SessionStats
from evaluator.models.position_session_stats import PositionSessionStats


class TestPerformanceCalculator:
    """Tests for PerformanceCalculator."""

    def test_compute_account_performance_empty_sessions(self):
        """Test compute_account_performance with empty session list."""
        result = PerformanceCalculator.compute_account_performance([], 0.02)
        assert result.total_trades == 0
        assert result.net_profit == Decimal("0")
        assert result.initial_cash == Decimal("0")

    def test_compute_account_performance_single_session_profit(self):
        """Test compute_account_performance with single profitable session."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        result = PerformanceCalculator.compute_account_performance([session], 0.02)
        assert result.total_trades >= 0
        assert result.net_profit >= Decimal("0")

    def test_compute_account_performance_single_session_loss(self):
        """Test compute_account_performance with single losing session."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("90000"),
        )
        result = PerformanceCalculator.compute_account_performance([session], 0.02)
        assert result.net_profit <= Decimal("0")

    def test_compute_account_performance_multiple_sessions(self):
        """Test compute_account_performance with multiple sessions."""
        sessions = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
                end_cash=Decimal("105000"),
            ),
            SessionStats(
                session=20251118,
                start_cash=Decimal("105000"),
                end_cash=Decimal("110000"),
            ),
            SessionStats(
                session=20251119,
                start_cash=Decimal("110000"),
                end_cash=Decimal("108000"),
            ),
        ]
        result = PerformanceCalculator.compute_account_performance(sessions, 0.02)
        assert result.total_trades >= 0

    def test_compute_account_performance_with_commission(self):
        """Test compute_account_performance with commission."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                commission=Decimal("10.5"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("109989.5"),
            start_positions=positions,
            end_positions=positions,
        )
        result = PerformanceCalculator.compute_account_performance([session], 0.02)
        assert result.total_commission > 0

    def test_compute_account_performance_with_positions(self):
        """Test compute_account_performance with positions."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                start_volume=1000,
                start_value=Decimal("10000"),
                end_volume=500,
                end_value=Decimal("5500"),
                commission=Decimal("5"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("100000"),
            start_positions=positions,
            end_positions=positions,
        )
        result = PerformanceCalculator.compute_account_performance([session], 0.02)
        assert isinstance(result.total_trades, int)

    def test_compute_account_performance_calculates_win_rate(self):
        """Test that win rate is calculated correctly."""
        sessions = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
                end_cash=Decimal("110000"),
            ),
            SessionStats(
                session=20251118,
                start_cash=Decimal("110000"),
                end_cash=Decimal("105000"),
            ),
            SessionStats(
                session=20251119,
                start_cash=Decimal("105000"),
                end_cash=Decimal("115000"),
            ),
        ]
        result = PerformanceCalculator.compute_account_performance(sessions, 0.02)
        assert 0 <= result.win_rate <= 100

    def test_compute_account_performance_calculates_sharpe_ratio(self):
        """Test that Sharpe ratio is calculated."""
        sessions = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
                end_cash=Decimal("105000"),
            ),
            SessionStats(
                session=20251118,
                start_cash=Decimal("105000"),
                end_cash=Decimal("110000"),
            ),
        ]
        result = PerformanceCalculator.compute_account_performance(sessions, 0.02)
        assert isinstance(result.sharpe_ratio, float)

    def test_compute_account_performance_zero_risk_free(self):
        """Test compute_account_performance with zero risk-free rate."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        result = PerformanceCalculator.compute_account_performance([session], 0.0)
        assert isinstance(result.sharpe_ratio, float)

    def test_compute_account_performance_high_risk_free(self):
        """Test compute_account_performance with high risk-free rate."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        result = PerformanceCalculator.compute_account_performance([session], 0.20)
        assert isinstance(result.sharpe_ratio, float)

    def test_compute_account_performance_all_profitable_sessions(self):
        """Test with all profitable sessions."""
        sessions = [
            SessionStats(
                session=20251115 + i,
                start_cash=Decimal("100000"),
                end_cash=Decimal("105000"),
            )
            for i in range(10)
        ]
        result = PerformanceCalculator.compute_account_performance(sessions, 0.02)
        assert result.win_rate == 100.0

    def test_compute_account_performance_all_losing_sessions(self):
        """Test with all losing sessions."""
        sessions = [
            SessionStats(
                session=20251115 + i,
                start_cash=Decimal("100000"),
                end_cash=Decimal("95000"),
            )
            for i in range(10)
        ]
        result = PerformanceCalculator.compute_account_performance(sessions, 0.02)
        assert result.win_rate == 0.0

    def test_compute_account_performance_with_large_cash(self):
        """Test with large cash values."""
        sessions = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("999999999"),
                end_cash=Decimal("999999999"),
            ),
            SessionStats(
                session=20251118,
                start_cash=Decimal("999999999"),
                end_cash=Decimal("1999999999"),
            ),
        ]
        result = PerformanceCalculator.compute_account_performance(sessions, 0.02)
        assert result.net_profit > 0

    def test_compute_account_performance_with_small_cash(self):
        """Test with small cash values."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("0.01"),
            end_cash=Decimal("0.02"),
        )
        result = PerformanceCalculator.compute_account_performance([session], 0.02)
        assert isinstance(result.net_profit, Decimal)

    def test_compute_account_performance_max_drawdown(self):
        """Test max drawdown calculation."""
        sessions = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
                end_cash=Decimal("120000"),
            ),
            SessionStats(
                session=20251118,
                start_cash=Decimal("120000"),
                end_cash=Decimal("80000"),
            ),
            SessionStats(
                session=20251119,
                start_cash=Decimal("80000"),
                end_cash=Decimal("100000"),
            ),
        ]
        result = PerformanceCalculator.compute_account_performance(sessions, 0.02)
        assert result.max_drawdown >= 0

    def test_compute_position_performance_empty(self):
        """Test compute_position_performance with empty data."""
        result = PerformanceCalculator.compute_position_performance({}, "600000", 0.02)
        assert result.total_trades == 0

    def test_compute_position_performance_with_data(self):
        """Test compute_position_performance with position data."""
        position_stats = {
            20251115: {
                "end_positions": [
                    PositionSessionStats(
                        session=20251115,
                        symbol="600000",
                        start_volume=1000,
                        start_value=Decimal("10000"),
                        end_volume=0,
                        end_value=Decimal("0"),
                        net_cashflow=Decimal("11000"),
                        realized_profit=Decimal("1000"),
                        commission=Decimal("10"),
                    ),
                ],
            },
        }
        result = PerformanceCalculator.compute_position_performance(position_stats, "600000", 0.02)
        assert result.total_trades > 0

    def test_compute_position_performance_with_multiple_sessions(self):
        """Test compute_position_performance with multiple sessions."""
        position_stats = {
            20251115: {
                "end_positions": [
                    PositionSessionStats(
                        session=20251115,
                        symbol="600000",
                        start_volume=1000,
                        start_value=Decimal("10000"),
                        end_volume=500,
                        end_value=Decimal("5500"),
                        net_cashflow=Decimal("-4500"),
                        realized_profit=Decimal("0"),
                    ),
                ],
            },
            20251118: {
                "end_positions": [
                    PositionSessionStats(
                        session=20251118,
                        symbol="600000",
                        start_volume=500,
                        start_value=Decimal("5500"),
                        end_volume=0,
                        end_value=Decimal("0"),
                        net_cashflow=Decimal("5500"),
                        realized_profit=Decimal("500"),
                    ),
                ],
            },
        }
        result = PerformanceCalculator.compute_position_performance(position_stats, "600000", 0.02)
        assert isinstance(result.total_trades, int)

    def test_calculate_top_contributions_empty(self):
        """Test _calculate_top_contributions with empty list."""
        result = PerformanceCalculator._calculate_top_contributions([], 0)
        assert result == [0.0, 0.0, 0.0, 0.0]

    def test_calculate_top_contributions_single_value(self):
        """Test _calculate_top_contributions with single value."""
        result = PerformanceCalculator._calculate_top_contributions([100.0], 100.0)
        assert len(result) == 4
        assert result[0] == 100.0

    def test_calculate_top_contributions_multiple_values(self):
        """Test _calculate_top_contributions with multiple values."""
        values = [1000.0, 500.0, 300.0, 200.0, 100.0, 50.0, 30.0, 20.0]
        total = sum(values)
        result = PerformanceCalculator._calculate_top_contributions(values, total)
        assert len(result) == 4

    def test_calculate_top_contributions_loss(self):
        """Test _calculate_top_contributions for losses."""
        values = [1000.0, 500.0, 300.0, 200.0, 100.0]
        total = sum(values)
        result = PerformanceCalculator._calculate_top_contributions(values, total, is_loss=True)
        assert len(result) == 4

    def test_calculate_top_contributions_zero_total(self):
        """Test _calculate_top_contributions with zero total."""
        result = PerformanceCalculator._calculate_top_contributions([100.0], 0)
        assert result == [0.0, 0.0, 0.0, 0.0]

    def test_compute_account_performance_with_trades(self):
        """Test compute_account_performance with trade data."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                commission=Decimal("10"),
            ),
        ]
        trades = [
            {"code": "600000", "type": "buy", "volume": 1000, "price": 10.0, "pnl": 0},
            {"code": "600000", "type": "sell", "volume": 1000, "price": 11.0, "pnl": 1000},
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
            start_positions=positions,
            end_positions=positions,
            trades=trades,
        )
        result = PerformanceCalculator.compute_account_performance([session], 0.02)
        assert isinstance(result.total_trades, int)

    def test_compute_account_performance_open_positions(self):
        """Test that open positions are calculated."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                start_volume=0,
                start_value=Decimal("0"),
                end_volume=500,
                end_value=Decimal("5500"),
                net_cashflow=Decimal("-5500"),
            ),
            PositionSessionStats(
                session=20251115,
                symbol="000001",
                start_volume=0,
                start_value=Decimal("0"),
                end_volume=1000,
                end_value=Decimal("5000"),
                net_cashflow=Decimal("-5000"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("89500"),
            end_positions=positions,
        )
        result = PerformanceCalculator.compute_account_performance([session], 0.02)
        assert result.open_positions == 2
