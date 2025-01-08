from dash import html
import dash_bootstrap_components as dbc
from quantstats import stats
import pandas as pd
from typing import Dict

class PortfolioMetrics:
    def __init__(self, colors: Dict[str, str]):
        self.colors = colors

    def create_metric_card(self, title: str, value: str, description: str, 
                          icon: str, color: str) -> dbc.Card:
        """Create a metric card component."""
        return dbc.Card([
            dbc.CardBody([
                html.I(className=f"fas {icon} fa-2x mb-3", 
                      style={'color': self.colors[color]}),
                html.H4(title, className="text-muted"),
                html.H2(value, style={'color': self.colors[color]}),
                html.P(description, className="text-muted small")
            ])
        ], className="text-center h-100 shadow-sm metric-card", 
        style={'transition': 'all 0.3s ease-in-out',
               'border': 'none',
               'border-radius': '10px',
               'background': 'white',
               'cursor': 'pointer'})

    def create_all_metric_cards(self, port_ret: pd.Series) -> list:
        """Create all metric cards for the dashboard."""
        metrics = [
            {
                'title': 'Sharpe Ratio',
                'value': f"{stats.sharpe(port_ret):.3g}",
                'description': 'Risk-adjusted return measure',
                'icon': 'fa-chart-line',
                'color': 'primary'
            },
            {
                'title': 'Sortino Ratio',
                'value': f"{stats.sortino(port_ret):.3g}",
                'description': 'Downside risk-adjusted return',
                'icon': 'fa-shield-alt',
                'color': 'success'
            },
            {
                'title': 'CAGR',
                'value': f"{stats.cagr(port_ret):.1%}",
                'description': 'Compound Annual Growth Rate',
                'icon': 'fa-chart-area',
                'color': 'info'
            },
            {
                'title': 'Max Drawdown',
                'value': f"{stats.max_drawdown(port_ret):.1%}",
                'description': 'Largest peak-to-trough decline',
                'icon': 'fa-arrow-down',
                'color': 'danger'
            },
            {
                'title': 'Win Rate',
                'value': f"{stats.win_rate(port_ret):.1%}",
                'description': 'Percentage of positive returns',
                'icon': 'fa-trophy',
                'color': 'warning'
            }
        ]
        
        return [self.create_metric_card(**metric) for metric in metrics]
