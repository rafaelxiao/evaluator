from pydantic import BaseModel, Field, computed_field
from decimal import Decimal
from typing import Optional


class PositionSessionStats(BaseModel):
    """
    表示单个持仓标的在单个交易日的绩效数据。
    """

    session: int = Field(description="交易日期")
    symbol: str = Field(description="股票代码")
    start_volume: int = Field(default=0, description="期初持仓量")
    start_value: Decimal = Field(default=Decimal("0"), description="期初市值")
    end_volume: int = Field(default=0, description="期末持仓量")
    end_value: Decimal = Field(default=Decimal("0"), description="期末市值")
    net_cashflow: Decimal = Field(default=Decimal("0"), description="净现金流：加仓消耗现金(负)，平仓产生现金(正)")
    realized_profit: Decimal = Field(default=Decimal("0"), description="已实现盈亏：卖出liquid_value - 持仓成本(carry_price * volume)")
    end_market_price: Optional[Decimal] = Field(default=None, description="期末市价(仅在线模式且持仓未完全平仓时可用)")
    last_buy_price: Optional[Decimal] = Field(default=None, description="最后一次买入价格(用于回测对比)")
    commission: Decimal = Field(default=Decimal("0"), description="该持仓在该时段内的手续费总和")
    trade_count: int = Field(default=0, description="该时段内的交易次数(订单数)")

    model_config = {"frozen": True}

    @computed_field
    @property
    def profit_loss(self) -> Decimal:
        """盈亏金额 = 已实现盈亏"""
        return self.realized_profit

    @computed_field
    @property
    def profit_loss_ratio(self) -> Decimal:
        """盈亏比例 = 盈亏金额 / 期初市值"""
        if self.start_value == 0:
            return Decimal("0")
        return self.profit_loss / self.start_value

    @computed_field
    @property
    def market_value(self) -> Optional[Decimal]:
        """期末市值 = 期末持仓量 * 期末市价(仅当有市价时可用)"""
        if self.end_market_price is None:
            return None
        return self.end_volume * self.end_market_price

    @computed_field
    @property
    def average_price(self) -> Optional[Decimal]:
        """持仓均价 = (期初市值 + 净现金流) / 期初持仓量"""
        if self.start_volume == 0:
            return None
        return (self.start_value + self.net_cashflow) / self.start_volume
