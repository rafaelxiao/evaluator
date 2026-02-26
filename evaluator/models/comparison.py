from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List

from .performance import Performance


class SessionComparison(BaseModel):
    session: int

    first_pnl: Decimal
    first_pnl_pct: float
    first_trade_count: int
    first_end_cash: Decimal

    second_pnl: Decimal
    second_pnl_pct: float
    second_trade_count: int
    second_end_cash: Decimal

    pnl_delta: Decimal
    pnl_pct_delta: float
    trade_count_delta: int

    drift_ratio: float = Field(description="|pnl_delta| / |first_pnl|")


class PerformanceComparison(BaseModel):
    first: Performance
    second: Performance

    net_profit_delta: Decimal
    net_profit_pct_delta: float
    win_rate_delta: float
    sharpe_ratio_delta: float
    max_drawdown_delta: Decimal
    total_trades_delta: int

    performance_ratio: float = Field(
        description="second.net_profit / first.net_profit"
    )
    drift_percentage: float = Field(
        description="Overall drift: |delta| / |first| * 100"
    )

    sessions: List[SessionComparison] = Field(default_factory=list)

    total_sessions: int
    matched_sessions: int
    session_match_rate: float
