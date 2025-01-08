import plotly.graph_objects as go
import pandas as pd
from typing import Dict

class PortfolioCharts:
    def __init__(self, colors: Dict[str, str]):
        self.colors = colors

    def create_cumulative_returns_chart(self, port_ret: pd.Series) -> go.Figure:
        """Create cumulative returns chart."""
        return go.Figure(
            data=[go.Scatter(
                x=port_ret.index,
                y=(1 + port_ret).cumprod(),
                mode='lines',
                name='Portfolio',
                line=dict(color=self.colors['primary'])
            )],
            layout=go.Layout(
                title='Cumulative Portfolio Returns',
                yaxis=dict(title='Value'),
                template='plotly_white',
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
        )

    def create_rolling_stats_chart(self, port_ret: pd.Series) -> go.Figure:
        """Create rolling statistics chart."""
        return go.Figure(
            data=[
                go.Scatter(
                    x=port_ret.index,
                    y=port_ret.rolling(window=252).mean(),
                    mode='lines',
                    name='Rolling Mean',
                    line=dict(color=self.colors['success'])
                ),
                go.Scatter(
                    x=port_ret.index,
                    y=port_ret.rolling(window=252).std(),
                    mode='lines',
                    name='Rolling Volatility',
                    line=dict(color=self.colors['danger'])
                )
            ],
            layout=go.Layout(
                title='Rolling Mean Return and Volatility',
                yaxis=dict(title='Value'),
                template='plotly_white',
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
        )

    def create_drawdown_chart(self, port_ret: pd.Series) -> go.Figure:
        """Create drawdown chart."""
        return go.Figure(
            data=[go.Scatter(
                x=port_ret.index,
                y=((1 + port_ret).cumprod() / (1 + port_ret).cumprod().expanding().max() - 1),
                mode='lines',
                name='Drawdown',
                fill='tozeroy',
                line=dict(color=self.colors['danger'])
            )],
            layout=go.Layout(
                title='Portfolio Drawdown',
                yaxis=dict(title='Drawdown'),
                template='plotly_white',
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
        )

    def create_risk_metrics_chart(self, risk_metrics: Dict[str, float]) -> go.Figure:
        """Create risk metrics comparison chart."""
        return go.Figure(
            data=[go.Bar(
                x=list(risk_metrics.keys()),
                y=list(map(abs, risk_metrics.values())),
                text=[f'{v:.1%}' for v in risk_metrics.values()],
                textposition='auto',
                marker_color=[self.colors['info'], self.colors['warning'], self.colors['danger']]
            )],
            layout=go.Layout(
                title='Risk Metrics Comparison',
                yaxis=dict(title='Absolute Value'),
                template='plotly_white',
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
        )
