"""Tests for PositionSessionStats model."""
from decimal import Decimal
import pytest
from evaluator.models.position_session_stats import PositionSessionStats


class TestPositionSessionStats:
    """Tests for PositionSessionStats model."""

    def test_position_session_stats_full_init(self):
        """Test creating PositionSessionStats with all fields."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=1000,
            start_value=Decimal("10000"),
            end_volume=500,
            end_value=Decimal("5500"),
            net_cashflow=Decimal("-4500"),
            realized_profit=Decimal("500"),
            end_market_price=Decimal("11.0"),
            last_buy_price=Decimal("10.5"),
            commission=Decimal("10.0"),
            trade_count=2,
        )
        assert pos.session == 20251115
        assert pos.symbol == "600000"
        assert pos.start_volume == 1000
        assert pos.start_value == Decimal("10000")
        assert pos.end_volume == 500
        assert pos.end_value == Decimal("5500")
        assert pos.net_cashflow == Decimal("-4500")
        assert pos.realized_profit == Decimal("500")
        assert pos.end_market_price == Decimal("11.0")
        assert pos.last_buy_price == Decimal("10.5")
        assert pos.commission == Decimal("10.0")
        assert pos.trade_count == 2

    def test_position_session_stats_minimal_init(self):
        """Test creating PositionSessionStats with minimal fields."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
        )
        assert pos.session == 20251115
        assert pos.symbol == "600000"
        assert pos.start_volume == 0
        assert pos.start_value == Decimal("0")
        assert pos.end_volume == 0
        assert pos.end_value == Decimal("0")
        assert pos.net_cashflow == Decimal("0")
        assert pos.realized_profit == Decimal("0")
        assert pos.end_market_price is None
        assert pos.last_buy_price is None
        assert pos.commission == Decimal("0")
        assert pos.trade_count == 0

    def test_position_session_stats_profit_loss(self):
        """Test profit_loss computed property."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            realized_profit=Decimal("500"),
        )
        assert pos.profit_loss == Decimal("500")

    def test_position_session_stats_profit_loss_ratio(self):
        """Test profit_loss_ratio computed property."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_value=Decimal("10000"),
            realized_profit=Decimal("500"),
        )
        assert pos.profit_loss_ratio == Decimal("0.05")

    def test_position_session_stats_profit_loss_ratio_zero_start_value(self):
        """Test profit_loss_ratio when start_value is zero."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_value=Decimal("0"),
            realized_profit=Decimal("500"),
        )
        assert pos.profit_loss_ratio == Decimal("0")

    def test_position_session_stats_market_value_with_price(self):
        """Test market_value computed property with end_market_price."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            end_volume=500,
            end_market_price=Decimal("11.0"),
        )
        assert pos.market_value == Decimal("5500")

    def test_position_session_stats_market_value_without_price(self):
        """Test market_value computed property without end_market_price."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            end_volume=500,
        )
        assert pos.market_value is None

    def test_position_session_stats_average_price_with_volume(self):
        """Test average_price computed property with start_volume."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=1000,
            start_value=Decimal("10000"),
            net_cashflow=Decimal("-5000"),
        )
        assert pos.average_price == Decimal("5.0")

    def test_position_session_stats_average_price_zero_volume(self):
        """Test average_price when start_volume is zero."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=0,
            start_value=Decimal("10000"),
            net_cashflow=Decimal("-5000"),
        )
        assert pos.average_price is None

    def test_position_session_stats_frozen(self):
        """Test that PositionSessionStats is immutable."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=1000,
        )
        with pytest.raises(Exception):
            pos.start_volume = 2000

    def test_position_session_stats_buy_transaction(self):
        """Test a buy transaction scenario."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=0,
            start_value=Decimal("0"),
            end_volume=1000,
            end_value=Decimal("10500"),
            net_cashflow=Decimal("-10500"),
            realized_profit=Decimal("0"),
            commission=Decimal("10.5"),
            trade_count=1,
        )
        assert pos.net_cashflow < 0
        assert pos.realized_profit == Decimal("0")

    def test_position_session_stats_sell_transaction(self):
        """Test a sell transaction scenario."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=1000,
            start_value=Decimal("10000"),
            end_volume=0,
            end_value=Decimal("0"),
            net_cashflow=Decimal("10490"),
            realized_profit=Decimal("500"),
            commission=Decimal("10"),
            trade_count=1,
        )
        assert pos.net_cashflow > 0
        assert pos.realized_profit == Decimal("500")

    def test_position_session_stats_round_trip(self):
        """Test a round-trip: buy then sell."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=1000,
            start_value=Decimal("10000"),
            end_volume=1000,
            end_value=Decimal("11000"),
            net_cashflow=Decimal("0"),
            realized_profit=Decimal("0"),
            commission=Decimal("20"),
            trade_count=2,
        )
        assert pos.realized_profit == Decimal("0")

    def test_position_session_stats_with_none_prices(self):
        """Test PositionSessionStats with None for optional prices."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=1000,
            end_volume=800,
            end_market_price=None,
            last_buy_price=None,
        )
        assert pos.market_value is None

    def test_position_session_stats_various_symbols(self):
        """Test PositionSessionStats with different stock symbols."""
        symbols = ["600000", "000001", "300750", "688001", "SH600000", "SZ000001"]
        for symbol in symbols:
            pos = PositionSessionStats(
                session=20251115,
                symbol=symbol,
            )
            assert pos.symbol == symbol

    def test_position_session_stats_large_volume(self):
        """Test PositionSessionStats with large volumes."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=10_000_000,
            start_value=Decimal("100000000"),
            end_volume=5_000_000,
            end_value=Decimal("55000000"),
            net_cashflow=Decimal("-45000000"),
            realized_profit=Decimal("0"),
            commission=Decimal("100000"),
            trade_count=100,
        )
        assert pos.start_volume == 10_000_000

    def test_position_session_stats_decimal_precision(self):
        """Test PositionSessionStats with high decimal precision."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_value=Decimal("12345.678901234"),
            end_value=Decimal("23456.789012345"),
            net_cashflow=Decimal("-11111.111111111"),
            realized_profit=Decimal("123.456789012"),
            commission=Decimal("12.345678901"),
            end_market_price=Decimal("23.456789012"),
            last_buy_price=Decimal("12.345678901"),
        )
        assert pos.start_value == Decimal("12345.678901234")
        assert pos.end_value == Decimal("23456.789012345")

    def test_position_session_stats_edge_case_zero_end(self):
        """Test PositionSessionStats when everything is zero at end."""
        pos = PositionSessionStats(
            session=20251115,
            symbol="600000",
            start_volume=0,
            start_value=Decimal("0"),
            end_volume=0,
            end_value=Decimal("0"),
            net_cashflow=Decimal("0"),
            realized_profit=Decimal("0"),
            commission=Decimal("0"),
            trade_count=0,
        )
        assert pos.profit_loss == Decimal("0")
        assert pos.profit_loss_ratio == Decimal("0")
