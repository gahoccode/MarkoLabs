import dash
from dash import html, dcc, ALL
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from quantstats import stats
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import os

# Import our modular components
from src.config import COLORS, DATA_PATH
from src.data.loader import PortfolioDataLoader
from src.components.charts import PortfolioCharts
from src.components.metrics import PortfolioMetrics
from src.layouts.dashboard import DashboardLayout

# Initialize components
data_loader = PortfolioDataLoader(DATA_PATH)
returns, port_ret = data_loader.calculate_returns()
charts = PortfolioCharts(COLORS)
metrics = PortfolioMetrics(COLORS)
layout = DashboardLayout()

# Initialize Dash app with callback exception suppression
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.FLATLY,
        {
            'href': 'https://use.fontawesome.com/releases/v5.15.4/css/all.css',
            'rel': 'stylesheet',
            'integrity': 'sha384-DyZ88mC6Up2uqS4h/KRgHuoeGwBcD4Ng9SiP4dIRy0EXTlnuz47vAwmeGwVChigm',
            'crossorigin': 'anonymous'
        },
        {
            'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
            'rel': 'stylesheet',
            'integrity': 'sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3',
            'crossorigin': 'anonymous'
        },
        {'href': '/assets/styles.css', 'rel': 'stylesheet'}  
    ],
    suppress_callback_exceptions=True,
    assets_folder='assets'
)

# Create initial charts and metrics
initial_metric_cards = metrics.create_all_metric_cards(port_ret)
initial_chart_figures = {
    'Cumulative Returns': charts.create_cumulative_returns_chart(port_ret),
    'Rolling Statistics': charts.create_rolling_stats_chart(port_ret),
    'Drawdown Analysis': charts.create_drawdown_chart(port_ret),
    'Risk Metrics': charts.create_risk_metrics_chart({
        'Monthly VaR': stats.var(port_ret),
        'Monthly CVaR': stats.cvar(port_ret),
        'Max Drawdown': stats.max_drawdown(port_ret)
    })
}

# Create weight input components
def create_weight_inputs():
    asset_names = data_loader.asset_names
    current_weights = data_loader.weights
    
    return dbc.Card([
        dbc.CardHeader("Portfolio Weights", className="text-center"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label(f"{asset} Weight"),
                    dbc.Input(
                        id={'type': 'weight-input', 'index': i},
                        type='number',
                        min=0,
                        max=1,
                        step=0.1,
                        value=weight
                    )
                ], width=12, md=4, className="mb-3")
                for i, (asset, weight) in enumerate(zip(asset_names, current_weights))
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Update Portfolio", id='update-portfolio', color="primary", className="w-100"),
                    html.Div(id="weight-error", className="text-danger small mt-2")
                ], width=12)
            ])
        ])
    ], className="mb-4")

# Create file upload component
def create_upload_section():
    return dbc.Card([
        dbc.CardHeader("Data Upload", className="text-center"),
        dbc.CardBody([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select CSV File')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px 0'
                },
                multiple=False
            ),
            html.Div(id='upload-error', className="text-danger small mt-2"),
            html.Div(id='upload-success', className="text-success small mt-2")
        ])
    ], className="mb-4")

# Create app layout with initial content
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Portfolio Statistics", className="text-center my-4"), width=12)
    ]),
    create_upload_section(),
    html.Div(create_weight_inputs(), id='weight-inputs-container'),
    html.Div(layout.create_layout(initial_metric_cards, initial_chart_figures), id='charts-container')
], fluid=True)

# Callback to update the dashboard
@app.callback(
    [
        Output('weight-inputs-container', 'children'),
        Output('charts-container', 'children'),
        Output('upload-error', 'children'),
        Output('upload-success', 'children')
    ],
    [
        Input('upload-data', 'contents'),
        Input('update-portfolio', 'n_clicks')
    ],
    [
        State('upload-data', 'filename'),
        State({'type': 'weight-input', 'index': ALL}, 'value')
    ],
    prevent_initial_call=True
)
def update_dashboard(contents, n_clicks, filename, weights):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'] if ctx.triggered else None

    try:
        # Handle file upload
        if trigger_id == 'upload-data.contents' and contents is not None:
            # Validate the uploaded file
            is_valid, error_message = data_loader.validate_csv(contents, filename)
            if not is_valid:
                return dash.no_update, dash.no_update, error_message, ""

            # Load new data
            data_loader.load_data(contents, filename)
            success_msg = f"Successfully loaded {filename}"
        else:
            success_msg = ""

        # Handle weight updates
        if trigger_id == 'update-portfolio.n_clicks' and weights:
            try:
                weights = [float(w) if w is not None else 0 for w in weights]
                data_loader.set_weights(weights)
            except ValueError as e:
                return dash.no_update, dash.no_update, str(e), ""

        # Calculate portfolio returns
        returns, port_ret = data_loader.calculate_returns()

        # Create weight inputs section
        weight_inputs = create_weight_inputs()

        # Create charts and metrics
        metric_cards = metrics.create_all_metric_cards(port_ret)
        chart_figures = {
            'Cumulative Returns': charts.create_cumulative_returns_chart(port_ret),
            'Rolling Statistics': charts.create_rolling_stats_chart(port_ret),
            'Drawdown Analysis': charts.create_drawdown_chart(port_ret),
            'Risk Metrics': charts.create_risk_metrics_chart({
                'Monthly VaR': stats.var(port_ret),
                'Monthly CVaR': stats.cvar(port_ret),
                'Max Drawdown': stats.max_drawdown(port_ret)
            })
        }

        # Create layout components
        charts_layout = layout.create_layout(metric_cards, chart_figures)

        return weight_inputs, charts_layout, "", success_msg

    except Exception as e:
        return dash.no_update, dash.no_update, f"Error: {str(e)}", ""

if __name__ == '__main__':
    # Get host and port from environment variables with defaults
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8050))
    debug = os.getenv('DASH_DEBUG_MODE', 'False').lower() == 'true'
    
    app.run_server(
        host=host,
        port=port,
        debug=debug
    )
