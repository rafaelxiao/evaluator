"""Tests for SessionStats model."""
from decimal import Decimal
import pytest
from evaluator.models.session_stats import SessionStats
from evaluator.models.position_session_stats import PositionSessionStats


class TestSessionStats:
    """Tests for SessionStats model."""

    def test_session_stats_full_init(self):
        """Test creating SessionStats with all fields."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                start_volume=1000,
                start_value=Decimal("10000"),
                end_volume=500,
                end_value=Decimal("5500"),
                net_cashflow=Decimal("-4500"),
                realized_profit=Decimal("500"),
                commission=Decimal("10"),
            ),
            PositionSessionStats(
                session=20251115,
                symbol="000001",
                start_volume=2000,
                start_value=Decimal("20000"),
                end_volume=2000,
                end_value=Decimal("22000"),
                net_cashflow=Decimal("0"),
                realized_profit=Decimal("0"),
                commission=Decimal("20"),
            ),
        ]
        trades = [
            {"code": "600000", "type": "buy", "volume": 1000, "price": 10.0, "pnl": 0},
            {"code": "600000", "type": "sell", "volume": 500, "price": 11.0, "pnl": 500},
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("95000"),
            start_positions=positions,
            end_positions=positions,
            trades=trades,
        )
        assert session.session == 20251115
        assert session.start_cash == Decimal("100000")
        assert session.end_cash == Decimal("95000")
        assert len(session.start_positions) == 2
        assert len(session.trades) == 2

    def test_session_stats_minimal_init(self):
        """Test creating SessionStats with minimal fields."""
        session = SessionStats(
            session=20251115,
        )
        assert session.session == 20251115
        assert session.start_cash == Decimal("0")
        assert session.end_cash == Decimal("0")
        assert session.start_positions == []
        assert session.end_positions == []
        assert session.trades == []

    def test_session_stats_total_commission(self):
        """Test total_commission computed property (sums both start and end positions)."""
        start_positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                commission=Decimal("10.5"),
            ),
        ]
        end_positions = [
            PositionSessionStats(
                session=20251115,
                symbol="000001",
                commission=Decimal("20.3"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_positions=start_positions,
            end_positions=end_positions,
        )
        assert session.total_commission == Decimal("30.8")

    def test_session_stats_total_commission_empty(self):
        """Test total_commission when no positions."""
        session = SessionStats(session=20251115)
        assert session.total_commission == Decimal("0")

    def test_session_stats_total_net_cashflow(self):
        """Test total_net_cashflow computed property."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                net_cashflow=Decimal("-1000"),
            ),
            PositionSessionStats(
                session=20251115,
                symbol="000001",
                net_cashflow=Decimal("500"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_positions=positions,
        )
        assert session.total_net_cashflow == Decimal("-500")

    def test_session_stats_computed_end_cash(self):
        """Test computed_end_cash when end_cash is 0."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                net_cashflow=Decimal("-1000"),
                commission=Decimal("10"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("0"),
            start_positions=positions,
        )
        assert session.computed_end_cash == Decimal("98990")

    def test_session_stats_effective_end_cash_with_value(self):
        """Test effective_end_cash when end_cash is provided."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("95000"),
        )
        assert session.effective_end_cash == Decimal("95000")

    def test_session_stats_effective_end_cash_zero(self):
        """Test effective_end_cash when end_cash is 0."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("0"),
        )
        assert session.effective_end_cash == Decimal("100000")

    def test_session_stats_start_market_value(self):
        """Test start_market_value computed property."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                start_volume=1000,
                start_value=Decimal("10000"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            start_positions=positions,
        )
        assert session.start_market_value == Decimal("110000")

    def test_session_stats_start_market_value_no_positions(self):
        """Test start_market_value when no positions."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
        )
        assert session.start_market_value == Decimal("100000")

    def test_session_stats_end_market_value_with_market_price(self):
        """Test end_market_value when market_price is available."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                end_volume=500,
                end_market_price=Decimal("11.0"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            end_cash=Decimal("0"),
            end_positions=positions,
        )
        assert session.end_market_value == Decimal("5500")

    def test_session_stats_end_market_value_with_end_value(self):
        """Test end_market_value when only end_value is available."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                end_volume=500,
                end_value=Decimal("5500"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            end_cash=Decimal("95000"),
            end_positions=positions,
        )
        assert session.end_market_value == Decimal("100500")

    def test_session_stats_end_market_value_no_value(self):
        """Test end_market_value when no positions."""
        session = SessionStats(
            session=20251115,
            end_cash=Decimal("100000"),
        )
        assert session.end_market_value == Decimal("100000")

    def test_session_stats_profit_loss(self):
        """Test profit_loss computed property."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        assert session.profit_loss == Decimal("10000")

    def test_session_stats_profit_loss_ratio(self):
        """Test profit_loss_ratio computed property."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        assert session.profit_loss_ratio == Decimal("0.1")

    def test_session_stats_profit_loss_ratio_zero_start(self):
        """Test profit_loss_ratio when start_cash is 0."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("0"),
            end_cash=Decimal("10000"),
        )
        assert session.profit_loss_ratio == Decimal("0")

    def test_session_stats_cash_pnl(self):
        """Test cash_pnl computed property."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110000"),
        )
        assert session.cash_pnl == Decimal("10000")

    def test_session_stats_realized_pnl(self):
        """Test realized_pnl computed property."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                net_cashflow=Decimal("500"),
            ),
            PositionSessionStats(
                session=20251115,
                symbol="000001",
                net_cashflow=Decimal("-200"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_positions=positions,
        )
        assert session.realized_pnl == Decimal("300")

    def test_session_stats_frozen(self):
        """Test that SessionStats is immutable."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
        )
        with pytest.raises(Exception):
            session.session = 20251116

    def test_session_stats_with_trades(self):
        """Test SessionStats with trade records."""
        trades = [
            {"code": "600000", "type": "buy", "volume": 1000, "price": 10.0, "pnl": 0},
            {"code": "600000", "type": "sell", "volume": 1000, "price": 11.0, "pnl": 1000},
            {"code": "000001", "type": "buy", "volume": 2000, "price": 5.0, "pnl": 0},
        ]
        session = SessionStats(
            session=20251115,
            trades=trades,
        )
        assert len(session.trades) == 3

    def test_session_stats_empty_positions(self):
        """Test SessionStats with empty position lists."""
        session = SessionStats(
            session=20251115,
            start_positions=[],
            end_positions=[],
        )
        assert session.total_commission == Decimal("0")
        assert session.total_net_cashflow == Decimal("0")

    def test_session_stats_mixed_position_changes(self):
        """Test SessionStats with various position changes."""
        start_positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                start_volume=1000,
                start_value=Decimal("10000"),
            ),
        ]
        end_positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                end_volume=500,
                end_value=Decimal("5000"),
                net_cashflow=Decimal("-5000"),
                commission=Decimal("5"),
            ),
            PositionSessionStats(
                session=20251115,
                symbol="000001",
                end_volume=2000,
                end_value=Decimal("22000"),
                net_cashflow=Decimal("-22000"),
                commission=Decimal("22"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_positions=start_positions,
            end_positions=end_positions,
        )
        assert session.total_commission == Decimal("27")

    def test_session_stats_large_values(self):
        """Test SessionStats with large monetary values."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("9999999999.99"),
            end_cash=Decimal("8888888888.88"),
        )
        assert session.cash_pnl == Decimal("-1111111111.11")

    def test_session_stats_very_small_values(self):
        """Test SessionStats with very small values."""
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("0.01"),
            end_cash=Decimal("0.02"),
        )
        assert session.cash_pnl == Decimal("0.01")

    def test_session_stats_start_market_value_zero_volume(self):
        """Test start_market_value when position has zero volume."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                start_volume=0,
                start_value=Decimal("10000"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            start_positions=positions,
        )
        assert session.start_market_value == Decimal("100000")

    def test_session_stats_end_market_value_none_price(self):
        """Test end_market_value when price is None but end_value exists."""
        positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                end_volume=500,
                end_value=Decimal("5500"),
                end_market_price=None,
            ),
        ]
        session = SessionStats(
            session=20251115,
            end_cash=Decimal("100000"),
            end_positions=positions,
        )
        assert session.end_market_value == Decimal("105500")

    def test_session_stats_comprehensive(self):
        """Comprehensive test with all computed properties."""
        start_positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                start_volume=1000,
                start_value=Decimal("10000"),
                commission=Decimal("10"),
            ),
        ]
        end_positions = [
            PositionSessionStats(
                session=20251115,
                symbol="600000",
                end_volume=0,
                end_value=Decimal("0"),
                net_cashflow=Decimal("10500"),
                realized_profit=Decimal("500"),
                commission=Decimal("10"),
            ),
        ]
        session = SessionStats(
            session=20251115,
            start_cash=Decimal("100000"),
            end_cash=Decimal("110480"),
            start_positions=start_positions,
            end_positions=end_positions,
        )
        assert session.total_commission == Decimal("20")
        assert session.total_net_cashflow == Decimal("10500")
        assert session.profit_loss == Decimal("480")
