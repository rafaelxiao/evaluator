"""Tests for RatioCalculator."""
import math
from decimal import Decimal
import pytest
from evaluator.calculators.ratio import RatioCalculator


class TestRatioCalculator:
    """Tests for RatioCalculator."""

    def test_compute_sharpe_ratio_basic(self):
        """Test basic Sharpe ratio calculation."""
        returns = [0.01, 0.02, -0.01, 0.03, 0.015]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert isinstance(result, float)
        assert result != 0

    def test_compute_sharpe_ratio_empty_returns(self):
        """Test Sharpe ratio with empty returns list."""
        returns = []
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert result == 0.0

    def test_compute_sharpe_ratio_zero_num_periods(self):
        """Test Sharpe ratio with zero num_periods."""
        returns = [0.01, 0.02, 0.03]
        risk_free_rate = 0.02
        num_periods = 0

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert result == 0.0

    def test_compute_sharpe_ratio_zero_mean(self):
        """Test Sharpe ratio when mean return is zero."""
        returns = [0.01, -0.01, 0.02, -0.02]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert result == 0.0

    def test_compute_sharpe_ratio_zero_std(self):
        """Test Sharpe ratio when standard deviation is zero."""
        returns = [0.02, 0.02, 0.02, 0.02]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert result == 0.0

    def test_compute_sharpe_ratio_single_return(self):
        """Test Sharpe ratio with single return."""
        returns = [0.05]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert isinstance(result, float)

    def test_compute_sharpe_ratio_high_returns(self):
        """Test Sharpe ratio with high returns."""
        returns = [0.1, 0.15, 0.2, 0.12, 0.18]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert result > 0

    def test_compute_sharpe_ratio_negative_returns(self):
        """Test Sharpe ratio with mostly negative returns."""
        returns = [-0.05, -0.03, -0.01, -0.02, -0.04]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert result < 0

    def test_compute_sharpe_ratio_zero_risk_free(self):
        """Test Sharpe ratio with zero risk-free rate."""
        returns = [0.01, 0.02, 0.03, 0.015, 0.025]
        risk_free_rate = 0.0
        num_periods = 250

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert isinstance(result, float)

    def test_compute_sharpe_ratio_large_periods(self):
        """Test Sharpe ratio with large number of periods."""
        returns = [0.001] * 1000
        risk_free_rate = 0.02
        num_periods = 25000

        result = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert isinstance(result, float)

    def test_compute_sortino_ratio_basic(self):
        """Test basic Sortino ratio calculation."""
        returns = [0.01, 0.02, -0.01, 0.03, 0.015]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sortino_ratio(returns, risk_free_rate, num_periods)
        assert isinstance(result, float)

    def test_compute_sortino_ratio_empty_returns(self):
        """Test Sortino ratio with empty returns list."""
        returns = []
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sortino_ratio(returns, risk_free_rate, num_periods)
        assert result == 0.0

    def test_compute_sortino_ratio_zero_num_periods(self):
        """Test Sortino ratio with zero num_periods."""
        returns = [0.01, 0.02, 0.03]
        risk_free_rate = 0.02
        num_periods = 0

        result = RatioCalculator.compute_sortino_ratio(returns, risk_free_rate, num_periods)
        assert result == 0.0

    def test_compute_sortino_ratio_no_downside(self):
        """Test Sortino ratio when there are no downside returns."""
        returns = [0.01, 0.02, 0.03, 0.015, 0.025]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sortino_ratio(returns, risk_free_rate, num_periods)
        assert result == 0.0

    def test_compute_sortino_ratio_zero_downside_std(self):
        """Test Sortino ratio when downside std is zero."""
        returns = [-0.01, -0.01, -0.01, 0.05]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sortino_ratio(returns, risk_free_rate, num_periods)
        assert isinstance(result, float)

    def test_compute_sortino_ratio_all_negative(self):
        """Test Sortino ratio with all negative returns."""
        returns = [-0.05, -0.03, -0.01, -0.02, -0.04]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sortino_ratio(returns, risk_free_rate, num_periods)
        assert isinstance(result, float)

    def test_compute_sortino_ratio_mixed_returns(self):
        """Test Sortino ratio with mixed returns."""
        returns = [0.05, -0.02, 0.03, -0.01, 0.04, -0.03, 0.02, -0.04]
        risk_free_rate = 0.02
        num_periods = 250

        result = RatioCalculator.compute_sortino_ratio(returns, risk_free_rate, num_periods)
        assert isinstance(result, float)

    def test_compute_calmar_ratio_basic(self):
        """Test basic Calmar ratio calculation."""
        net_profit = Decimal("10000")
        max_drawdown = Decimal("2000")

        result = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)
        assert result == 5.0

    def test_compute_calmar_ratio_zero_drawdown(self):
        """Test Calmar ratio with zero drawdown."""
        net_profit = Decimal("10000")
        max_drawdown = Decimal("0")

        result = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)
        assert result == 0.0

    def test_compute_calmar_ratio_negative_profit(self):
        """Test Calmar ratio with negative profit."""
        net_profit = Decimal("-5000")
        max_drawdown = Decimal("2000")

        result = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)
        assert result == -2.5

    def test_compute_calmar_ratio_large_values(self):
        """Test Calmar ratio with large values."""
        net_profit = Decimal("999999999.99")
        max_drawdown = Decimal("500000")

        result = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)
        assert result > 0

    def test_compute_calmar_ratio_small_values(self):
        """Test Calmar ratio with small values."""
        net_profit = Decimal("0.01")
        max_drawdown = Decimal("0.001")

        result = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)
        assert result == 10.0

    def test_compute_calmar_ratio_exact_division(self):
        """Test Calmar ratio with exact division."""
        net_profit = Decimal("100")
        max_drawdown = Decimal("25")

        result = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)
        assert result == 4.0

    def test_compute_sharpe_ratio_consistency(self):
        """Test Sharpe ratio consistency across multiple calls."""
        returns = [0.01, 0.02, -0.01, 0.03, 0.015]
        risk_free_rate = 0.02
        num_periods = 250

        result1 = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        result2 = RatioCalculator.compute_sharpe_ratio(returns, risk_free_rate, num_periods)
        assert result1 == result2

    def test_compute_sortino_ratio_consistency(self):
        """Test Sortino ratio consistency across multiple calls."""
        returns = [0.01, 0.02, -0.01, 0.03, 0.015]
        risk_free_rate = 0.02
        num_periods = 250

        result1 = RatioCalculator.compute_sortino_ratio(returns, risk_free_rate, num_periods)
        result2 = RatioCalculator.compute_sortino_ratio(returns, risk_free_rate, num_periods)
        assert result1 == result2

    def test_compute_calmar_ratio_consistency(self):
        """Test Calmar ratio consistency across multiple calls."""
        net_profit = Decimal("10000")
        max_drawdown = Decimal("2000")

        result1 = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)
        result2 = RatioCalculator.compute_calmar_ratio(net_profit, max_drawdown)
        assert result1 == result2

    def test_periods_per_year_constant(self):
        """Test that PERIODS_PER_YEAR is defined correctly."""
        assert RatioCalculator.PERIODS_PER_YEAR == 250
