from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, List
import plotly.graph_objects as go

class DashboardLayout:
    def __init__(self):
        self.custom_css = '''
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            }
        '''

    def create_header(self) -> dbc.Row:
        """Create dashboard header."""
        return dbc.Row([
            dbc.Col(html.H1("Portfolio Statistics", 
                           className="text-center my-4"), 
                   width=12)
        ])

    def create_metrics_section(self, metric_cards: List[dbc.Card]) -> dbc.Row:
        """Create metrics section with cards."""
        # Add IDs to metric cards for dynamic updates
        for i, card in enumerate(metric_cards):
            card.id = f'metric-{i}'
            
        # First three cards in one row
        first_row = dbc.Row([
            dbc.Col(card, width=12, lg=4, className="mb-4")
            for card in metric_cards[:3]
        ])
        
        # Last two cards in another row
        second_row = dbc.Row([
            dbc.Col(card, width=12, lg=6, className="mb-4")
            for card in metric_cards[3:]
        ])
        
        return html.Div([first_row, second_row])

    def create_chart_section(self, charts: Dict[str, go.Figure]) -> dbc.Row:
        """Create charts section."""
        chart_components = []
        for i, (title, figure) in enumerate(charts.items()):
            chart_components.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(title, className="text-center"),
                        dbc.CardBody([
                            dcc.Graph(
                                id=f'chart-{i}',
                                figure=figure
                            )
                        ])
                    ])
                ], width=12, className="mb-4")
            )
        
        return dbc.Row(chart_components)

    def create_layout(self, metric_cards: List[dbc.Card], 
                     charts: Dict[str, go.Figure]) -> dbc.Container:
        """Create main dashboard layout."""
        return dbc.Container([
            self.create_header(),
            self.create_metrics_section(metric_cards),
            self.create_chart_section(charts)
        ], fluid=True)
