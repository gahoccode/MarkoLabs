import plotly.io as pio

# Color palette
COLORS = {
    'primary': '#2C3E50',    # Dark blue-gray
    'success': '#18BC9C',    # Turquoise
    'info': '#3498DB',       # Blue
    'warning': '#F39C12',    # Orange
    'danger': '#E74C3C',     # Red
    'gray': '#95A5A6'        # Gray
}

# File paths
DATA_PATH = "F:/Data Science/CafeF.SolieuGD.Upto24092024/myport2.csv"

# Chart settings
pio.templates.default = "plotly_white"

# Portfolio settings
DEFAULT_WEIGHTS = [0.2, 0.3, 0.5]
