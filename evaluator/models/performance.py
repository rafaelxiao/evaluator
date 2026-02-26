from pydantic import BaseModel, Field
from decimal import Decimal


class Performance(BaseModel):
    """
    绩效统计基类。
    """

    total_trades: int = Field(..., description="Total number of trades")
    open_positions: int = Field(default=0, description="Number of open positions at end of backtest")
    winning_trades: int = Field(..., description="Number of winning trades")
    losing_trades: int = Field(..., description="Number of losing trades")
    win_rate: float = Field(..., description="Win rate percentage")
    net_profit: Decimal = Field(..., description="Net profit/loss")
    net_profit_pct: float = Field(..., description="Net profit percentage")
    max_drawdown: Decimal = Field(..., description="Maximum drawdown")
    sharpe_ratio: float = Field(..., description="Sharpe ratio")
    final_value: Decimal = Field(..., description="Final portfolio value")
    initial_cash: Decimal = Field(..., description="Initial cash")

    total_commission: Decimal = Field(default=Decimal("0"), description="Total commission paid")

    max_single_win: Decimal = Field(default=Decimal("0"), description="Maximum single trade win")
    max_single_loss: Decimal = Field(default=Decimal("0"), description="Maximum single trade loss")
    max_single_win_pct: float = Field(default=0.0, description="Maximum single trade win percentage")
    max_single_loss_pct: float = Field(default=0.0, description="Maximum single trade loss percentage")
    avg_win: Decimal = Field(default=Decimal("0"), description="Average winning trade amount")
    avg_loss: Decimal = Field(default=Decimal("0"), description="Average losing trade amount")
    avg_win_pct: float = Field(default=0.0, description="Average winning trade percentage")
    avg_loss_pct: float = Field(default=0.0, description="Average losing trade percentage")
    odds_ratio: float = Field(default=0.0, description="Average win / average loss")
    total_win: Decimal = Field(default=Decimal("0"), description="Total winning amount")
    total_loss: Decimal = Field(default=Decimal("0"), description="Total losing amount")

    max_drawdown_duration_bars: int = Field(default=0, description="Max drawdown duration in bars")
    commission_loss_pct: float = Field(default=0.0, description="Commission loss as % of total loss")

    top_1pct_win_pct: float = Field(default=0.0, description="Top 1% winning trades contribution to total return")
    top_5pct_win_pct: float = Field(default=0.0, description="Top 5% winning trades contribution to total return")
    top_10pct_win_pct: float = Field(default=0.0, description="Top 10% winning trades contribution to total return")
    top_20pct_win_pct: float = Field(default=0.0, description="Top 20% winning trades contribution to total return")

    top_1pct_loss_pct: float = Field(default=0.0, description="Top 1% losing trades contribution to total loss")
    top_5pct_loss_pct: float = Field(default=0.0, description="Top 5% losing trades contribution to total loss")
    top_10pct_loss_pct: float = Field(default=0.0, description="Top 10% losing trades contribution to total loss")
    top_20pct_loss_pct: float = Field(default=0.0, description="Top 20% losing trades contribution to total loss")

    sortino_ratio: float = Field(default=0.0, description="Sortino ratio")
    calmar_ratio: float = Field(default=0.0, description="Calmar ratio")
