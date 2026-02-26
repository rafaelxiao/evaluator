import math
from decimal import Decimal
from typing import List


class RatioCalculator:
    """比率计算器 - 计算夏普比率、索提诺比率、卡玛比率"""

    PERIODS_PER_YEAR = 250

    @staticmethod
    def compute_sharpe_ratio(
        returns: List[float],
        risk_free_rate: float,
        num_periods: int,
    ) -> float:
        """计算夏普比率"""
        if not returns or num_periods == 0:
            return 0.0

        mean_return = sum(returns) / len(returns)
        if mean_return == 0:
            return 0.0

        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = math.sqrt(variance)

        if std_dev == 0:
            return 0.0

        annual_rf = risk_free_rate
        period_rf = annual_rf / RatioCalculator.PERIODS_PER_YEAR

        excess_return = mean_return - period_rf
        annualized_excess = excess_return * math.sqrt(RatioCalculator.PERIODS_PER_YEAR)

        return annualized_excess / (std_dev * math.sqrt(RatioCalculator.PERIODS_PER_YEAR))

    @staticmethod
    def compute_sortino_ratio(
        returns: List[float],
        risk_free_rate: float,
        num_periods: int,
    ) -> float:
        """计算索提诺比率"""
        if not returns or num_periods == 0:
            return 0.0

        annual_rf = risk_free_rate
        period_rf = annual_rf / RatioCalculator.PERIODS_PER_YEAR

        mean_return = sum(returns) / len(returns)
        excess_return = mean_return - period_rf

        downside_returns = [r for r in returns if r < 0]
        if not downside_returns:
            return 0.0

        downside_variance = sum(r ** 2 for r in downside_returns) / len(downside_returns)
        downside_std = math.sqrt(downside_variance)

        if downside_std == 0:
            return 0.0

        annualized_excess = excess_return * math.sqrt(RatioCalculator.PERIODS_PER_YEAR)

        return annualized_excess / (downside_std * math.sqrt(RatioCalculator.PERIODS_PER_YEAR))

    @staticmethod
    def compute_calmar_ratio(
        net_profit: Decimal,
        max_drawdown: Decimal,
    ) -> float:
        """计算卡玛比率"""
        if max_drawdown == 0:
            return 0.0

        return float(net_profit / max_drawdown)
