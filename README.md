# MarkoLabs - Portfolio Analytics Dashboard

A modern, interactive dashboard for portfolio analysis built with Plotly Dash. This application allows users to upload portfolio data, visualize performance metrics, and dynamically adjust portfolio weights.

## Features

- Interactive data visualization with Plotly charts
- Dynamic portfolio weight adjustments
- Real-time performance metrics
- CSV file upload functionality
- Responsive design with Bootstrap components

## Project Structure

```
MarkoLabs/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── charts.py      # Chart creation components
│   │   └── metrics.py     # Portfolio metrics calculations
│   ├── data/
│   │   └── loader.py      # Data loading and processing
│   ├── layouts/
│   │   └── dashboard.py   # Dashboard layout components
│   └── config.py          # Configuration settings
├── dashboard.py           # Main application file
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MarkoLabs.git
cd MarkoLabs
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Docker Installation

1. Build and run using Docker Compose (recommended):
```bash
docker-compose up -d
```

2. Or build and run using Docker directly:
```bash
# Build the Docker image
docker build -t markolabs .

# Run the container
docker run -d -p 8051:8051 markolabs
```

3. Access the dashboard at `http://localhost:8051`

### Environment Variables

The application can be configured using the following environment variables:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8051)
- `DASH_DEBUG_MODE`: Enable debug mode (default: False)

These can be set in the docker-compose.yml file or passed directly to docker run:

```bash
docker run -d -p 8051:8051 -e PORT=8051 markolabs
```

## Usage

1. Start the dashboard:
```bash
python dashboard.py
```

2. Open your browser and navigate to `http://127.0.0.1:8051/`

3. Upload your portfolio data CSV file or use the default data

4. Adjust portfolio weights using the input fields and click "Update Portfolio"

## Data Format Requirements

### CSV File Structure

The CSV file should follow this format:

```csv
Date,Asset1,Asset2,Asset3,...
20240101,100.0,150.0,200.0,...
20240102,101.0,151.0,202.0,...
20240103,99.0,152.0,198.0,...
```

### Requirements:

1. **Date Column**:
   - Must be named exactly "Date"
   - Format: YYYYMMDD (e.g., 20240101)
   - Must be in chronological order

2. **Asset Columns**:
   - Each column represents one asset
   - Column names should be the asset identifiers
   - Values must be numeric (prices or returns)
   - No missing values allowed

3. **File Format**:
   - Must be a CSV file
   - UTF-8 encoding recommended
   - No special characters in column names

### Example Data:
```csv
Date,AAPL,GOOGL,MSFT
20240101,185.50,140.20,375.80
20240102,186.20,141.50,377.90
20240103,184.90,139.80,374.60
```

## Features and Functionality

### Portfolio Metrics
- Cumulative Returns
- Rolling Statistics
- Drawdown Analysis
- Risk Metrics (VaR, CVaR)
- Sharpe Ratio
- Maximum Drawdown

### Interactive Features
1. **Data Upload**:
   - Drag and drop CSV files
   - Automatic validation
   - Error messaging for invalid files

2. **Weight Adjustment**:
   - Individual asset weight inputs
   - Real-time validation
   - Automatic equal weight option

3. **Visualizations**:
   - Interactive charts
   - Hover tooltips
   - Zoom functionality
   - Download options

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Dependencies

- dash
- dash-bootstrap-components
- plotly
- pandas
- numpy
- quantstats
- python-dateutil

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Plotly Dash](https://dash.plotly.com/)
- Styled with [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- Portfolio analytics powered by [QuantStats](https://github.com/ranaroussi/quantstats)
