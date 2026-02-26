"""Tests for PerformanceEvaluator."""
from decimal import Decimal
import pytest
from evaluator.performance_evaluator import PerformanceEvaluator
from evaluator.models.session_stats import SessionStats
from evaluator.models.position_session_stats import PositionSessionStats
from evaluator.models.performance import Performance


class ConcretePerformanceEvaluator(PerformanceEvaluator):
    """Concrete implementation for testing."""
    pass


class TestPerformanceEvaluator:
    """Tests for PerformanceEvaluator."""

    def test_evaluate_empty_sessions(self):
        """Test evaluate with empty sessions list."""
        evaluator = ConcretePerformanceEvaluator(risk_free_rate=0.02)
        result = evaluator.evaluate([])
        assert isinstance(result, Performance)
        assert result.total_trades == 0

    def test_evaluate_single_session(self):
        """Test evaluate with single session."""
        evaluator = ConcretePerformanceEvaluator(risk_free_rate=0.02)
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        result = evaluator.evaluate([session])
        assert isinstance(result, Performance)

    def test_evaluate_multiple_sessions(self):
        """Test evaluate with multiple sessions."""
        evaluator = ConcretePerformanceEvaluator(risk_free_rate=0.02)
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
        result = evaluator.evaluate(sessions)
        assert isinstance(result, Performance)

    def test_evaluate_with_positions(self):
        """Test evaluate with positions."""
        evaluator = ConcretePerformanceEvaluator(risk_free_rate=0.02)
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                start_volume=1000,
                start_value=Decimal("10000"),
                end_volume=500,
                end_value=Decimal("5500"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("100000"),
            start_positions=positions,
            end_positions=positions,
        )
        result = evaluator.evaluate([session])
        assert isinstance(result, Performance)

    def test_evaluate_with_default_risk_free(self):
        """Test evaluate with default risk-free rate."""
        evaluator = ConcretePerformanceEvaluator()
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        result = evaluator.evaluate([session])
        assert isinstance(result, Performance)

    def test_evaluate_with_custom_risk_free(self):
        """Test evaluate with custom risk-free rate."""
        evaluator = ConcretePerformanceEvaluator(risk_free_rate=0.05)
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        result = evaluator.evaluate([session])
        assert isinstance(result, Performance)

    def test_evaluate_with_high_risk_free(self):
        """Test evaluate with high risk-free rate."""
        evaluator = ConcretePerformanceEvaluator(risk_free_rate=0.20)
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        result = evaluator.evaluate([session])
        assert isinstance(result, Performance)

    def test_evaluate_with_zero_risk_free(self):
        """Test evaluate with zero risk-free rate."""
        evaluator = ConcretePerformanceEvaluator(risk_free_rate=0.0)
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        result = evaluator.evaluate([session])
        assert isinstance(result, Performance)

    def test_compare_empty_sessions(self):
        """Test compare with empty sessions."""
        evaluator = ConcretePerformanceEvaluator()
        result = evaluator.compare([], [])
        assert isinstance(result.first, Performance)
        assert isinstance(result.second, Performance)
        assert result.total_sessions == 0

    def test_compare_identical_sessions(self):
        """Test compare with identical sessions."""
        evaluator = ConcretePerformanceEvaluator()
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
        result = evaluator.compare(sessions, sessions)
        assert result.performance_ratio == 1.0
        assert result.drift_percentage == 0.0

    def test_compare_different_sessions(self):
        """Test compare with different sessions."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
                end_cash=Decimal("110000"),
            ),
        ]
        sessions_b = [
            SessionStats(
                session=20251115,
                start_cash=Decimal("100000"),
                end_cash=Decimal("120000"),
            ),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert result.performance_ratio != 1.0

    def test_compare_multiple_sessions(self):
        """Test compare with multiple sessions."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("105000")),
            SessionStats(session=20251118, start_cash=Decimal("105000"), end_cash=Decimal("110000")),
        ]
        sessions_b = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("108000")),
            SessionStats(session=20251118, start_cash=Decimal("108000"), end_cash=Decimal("115000")),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert len(result.sessions) == 2

    def test_compare_partial_session_match(self):
        """Test compare with partial session match."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("110000")),
            SessionStats(session=20251116, start_cash=Decimal("110000"), end_cash=Decimal("120000")),
        ]
        sessions_b = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("108000")),
            SessionStats(session=20251117, start_cash=Decimal("108000"), end_cash=Decimal("115000")),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert result.matched_sessions == 1
        assert result.session_match_rate < 1.0

    def test_compare_no_common_sessions(self):
        """Test compare with no common sessions."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("110000")),
        ]
        sessions_b = [
            SessionStats(session=20251120, start_cash=Decimal("100000"), end_cash=Decimal("110000")),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert result.matched_sessions == 0
        assert result.session_match_rate == 0.0

    def test_compare_second_outperforms_first(self):
        """Test compare where second outperforms first."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("100000")),
            SessionStats(session=20251118, start_cash=Decimal("100000"), end_cash=Decimal("105000")),
        ]
        sessions_b = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("100000")),
            SessionStats(session=20251118, start_cash=Decimal("100000"), end_cash=Decimal("120000")),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert result.net_profit_delta > 0
        assert result.performance_ratio > 1.0

    def test_compare_first_outperforms_second(self):
        """Test compare where first outperforms second."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("100000")),
            SessionStats(session=20251118, start_cash=Decimal("100000"), end_cash=Decimal("120000")),
        ]
        sessions_b = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("100000")),
            SessionStats(session=20251118, start_cash=Decimal("100000"), end_cash=Decimal("105000")),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert result.net_profit_delta < 0
        assert result.performance_ratio < 1.0

    def test_compare_zero_net_profit(self):
        """Test compare with zero net profit."""
        evaluator = ConcretePerformanceEvaluator()
        sessions = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("100000")),
        ]
        result = evaluator.compare(sessions, sessions)
        assert result.performance_ratio == 0.0
        assert result.drift_percentage == 0.0

    def test_compare_win_rate_delta(self):
        """Test compare calculates win rate delta."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("110000")),
            SessionStats(session=20251118, start_cash=Decimal("110000"), end_cash=Decimal("95000")),
        ]
        sessions_b = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("120000")),
            SessionStats(session=20251118, start_cash=Decimal("120000"), end_cash=Decimal("110000")),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert isinstance(result.win_rate_delta, float)

    def test_compare_max_drawdown_delta(self):
        """Test compare calculates max drawdown delta."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("120000")),
            SessionStats(session=20251118, start_cash=Decimal("120000"), end_cash=Decimal("80000")),
        ]
        sessions_b = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("110000")),
            SessionStats(session=20251118, start_cash=Decimal("110000"), end_cash=Decimal("90000")),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert isinstance(result.max_drawdown_delta, Decimal)

    def test_evaluate_position_empty(self):
        """Test evaluate_position with empty data."""
        evaluator = ConcretePerformanceEvaluator()
        result = evaluator.evaluate_position({}, "600000")
        assert result.total_trades == 0

    def test_evaluate_position_with_data(self):
        """Test evaluate_position with position data."""
        evaluator = ConcretePerformanceEvaluator()
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
                    ),
                ],
            },
        }
        result = evaluator.evaluate_position(position_stats, "600000")
        assert isinstance(result, Performance)

    def test_evaluate_position_with_multiple_sessions(self):
        """Test evaluate_position with multiple sessions."""
        evaluator = ConcretePerformanceEvaluator()
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
        result = evaluator.evaluate_position(position_stats, "600000")
        assert isinstance(result, Performance)

    def test_compare_session_comparisons_not_empty(self):
        """Test that compare returns session comparisons."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("110000")),
            SessionStats(session=20251118, start_cash=Decimal("110000"), end_cash=Decimal("120000")),
        ]
        sessions_b = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("105000")),
            SessionStats(session=20251118, start_cash=Decimal("105000"), end_cash=Decimal("115000")),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert len(result.sessions) == 2

    def test_compare_total_sessions(self):
        """Test that total_sessions includes all unique sessions."""
        evaluator = ConcretePerformanceEvaluator()
        sessions_a = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("110000")),
            SessionStats(session=20251116, start_cash=Decimal("110000"), end_cash=Decimal("120000")),
        ]
        sessions_b = [
            SessionStats(session=20251115, start_cash=Decimal("100000"), end_cash=Decimal("108000")),
            SessionStats(session=20251117, start_cash=Decimal("108000"), end_cash=Decimal("115000")),
        ]
        result = evaluator.compare(sessions_a, sessions_b)
        assert result.total_sessions == 3

    def test_evaluate_with_commission(self):
        """Test evaluate with commission."""
        evaluator = ConcretePerformanceEvaluator()
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
        result = evaluator.evaluate([session])
        assert result.total_commission > 0
