from pydantic import BaseModel, Field, computed_field
from decimal import Decimal
from typing import List, Dict, Any

from .position_session_stats import PositionSessionStats


class SessionStats(BaseModel):
    """
    表示账户在单个交易日的绩效数据。
    """

    session: int = Field(description="交易日期")
    start_cash: Decimal = Field(default=Decimal("0"), description="期初现金")
    end_cash: Decimal = Field(default=Decimal("0"), description="期末现金")
    start_positions: List[PositionSessionStats] = Field(default_factory=list, description="期初持仓列表")
    end_positions: List[PositionSessionStats] = Field(default_factory=list, description="期末持仓列表")
    trades: List[Dict[str, Any]] = Field(default_factory=list, description="交易记录列表")

    model_config = {"frozen": True}

    @computed_field
    @property
    def total_commission(self) -> Decimal:
        """总手续费 = 所有持仓的手续费总和"""
        return sum(
            p.commission
            for p in self.start_positions + self.end_positions
        )

    @computed_field
    @property
    def total_net_cashflow(self) -> Decimal:
        """总净现金流 = 所有持仓的净现金流总和"""
        return sum(
            p.net_cashflow
            for p in self.start_positions + self.end_positions
        )

    @computed_field
    @property
    def computed_end_cash(self) -> Decimal:
        """计算的期末现金 = 期初现金 + 总净现金流 - 总手续费"""
        return self.start_cash + self.total_net_cashflow - self.total_commission

    @computed_field
    @property
    def effective_end_cash(self) -> Decimal:
        """有效期末现金 = 如果传入的end_cash非0则使用，否则用计算的"""
        return self.end_cash if self.end_cash != Decimal("0") else self.computed_end_cash

    @computed_field
    @property
    def start_market_value(self) -> Decimal:
        """期初市值 = 期初现金 + 期初持仓市值"""
        positions_value = Decimal("0")
        for p in self.start_positions:
            if p.start_volume != 0:
                positions_value += p.start_value
        return self.start_cash + positions_value

    @computed_field
    @property
    def end_market_value(self) -> Decimal:
        """期末市值 = 期末现金 + 期末持仓市值(如果有市价)"""
        positions_value = Decimal("0")
        for p in self.end_positions:
            if p.market_value is not None:
                positions_value += p.market_value
            elif p.end_volume != 0:
                positions_value += p.end_value
        return self.effective_end_cash + positions_value

    @computed_field
    @property
    def profit_loss(self) -> Decimal:
        """盈亏金额 = 期末市值 - 期初市值"""
        return self.end_market_value - self.start_market_value

    @computed_field
    @property
    def profit_loss_ratio(self) -> Decimal:
        """盈亏比例 = 盈亏金额 / 期初资金"""
        if self.start_cash == 0:
            return Decimal("0")
        return self.profit_loss / self.start_cash

    @computed_field
    @property
    def cash_pnl(self) -> Decimal:
        """现金盈亏 = 期末现金 - 期初现金"""
        return self.end_cash - self.start_cash

    @computed_field
    @property
    def realized_pnl(self) -> Decimal:
        """已实现盈亏 = 总净现金流"""
        return self.total_net_cashflow
