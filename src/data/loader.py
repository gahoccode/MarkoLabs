import pandas as pd
import numpy as np
import io
import base64
from typing import Tuple, Dict, List, Optional, Union

class PortfolioDataLoader:
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        self.df = None
        self.returns = None
        self._weights = None

    @property
    def weights(self) -> List[float]:
        """Get current portfolio weights."""
        return self._weights

    def set_weights(self, weights: Optional[List[float]] = None) -> None:
        """Set portfolio weights, validating they sum to 1."""
        if weights is None:
            # Default equal weights if none provided
            self.df = self.df if self.df is not None else self.load_data()
            n_assets = len(self.df.columns)
            self._weights = [1/n_assets] * n_assets
        else:
            # Validate weights
            if abs(sum(weights) - 1.0) > 1e-6:
                raise ValueError("Weights must sum to 1")
            self._weights = weights

    def load_data(self, contents: Optional[str] = None, filename: Optional[str] = None) -> pd.DataFrame:
        """
        Load and preprocess the portfolio data.
        
        Args:
            contents: Optional base64 encoded contents of uploaded file
            filename: Optional filename of uploaded file
        """
        try:
            if contents is not None:
                # Handle uploaded file
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                
                if filename.endswith('.csv'):
                    self.df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                else:
                    raise ValueError("Please upload a CSV file")
            elif self.file_path:
                # Load from file path
                self.df = pd.read_csv(self.file_path)
            else:
                raise ValueError("No data source provided")

            # Process the data
            if 'Date' not in self.df.columns:
                raise ValueError("CSV must contain a 'Date' column")

            self.df['Date'] = pd.to_datetime(self.df['Date'], format='%Y%m%d')
            self.df.set_index(['Date'], inplace=True)
            
            # Set equal weights if not already set
            if self._weights is None:
                self.set_weights()
                
            return self.df
            
        except Exception as e:
            raise ValueError(f"Error loading data: {str(e)}")

    def calculate_returns(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Calculate portfolio returns and statistics."""
        if self.df is None:
            self.load_data()
        
        self.returns = self.df.pct_change().dropna()
        weighted_returns = self.returns * self._weights
        port_ret = weighted_returns.sum(axis=1)
        
        return self.returns, port_ret

    @property
    def portfolio_weights(self) -> Dict[str, float]:
        """Return portfolio weights as a dictionary."""
        self.df = self.df if self.df is not None else self.load_data()
        return dict(zip(self.df.columns, self._weights))

    @property
    def asset_names(self) -> List[str]:
        """Get list of asset names."""
        self.df = self.df if self.df is not None else self.load_data()
        return list(self.df.columns)

    def validate_csv(self, contents: str, filename: str) -> Tuple[bool, str]:
        """
        Validate the uploaded CSV file.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            
            if not filename.endswith('.csv'):
                return False, "Please upload a CSV file"
                
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
            if 'Date' not in df.columns:
                return False, "CSV must contain a 'Date' column"
                
            # Try parsing dates
            try:
                pd.to_datetime(df['Date'], format='%Y%m%d')
            except:
                return False, "Date column must be in YYYYMMDD format"
                
            # Check for numeric columns (excluding Date)
            non_numeric = df.drop('Date', axis=1).select_dtypes(exclude=['float64', 'int64']).columns
            if len(non_numeric) > 0:
                return False, f"Columns must be numeric: {', '.join(non_numeric)}"
                
            return True, ""
            
        except Exception as e:
            return False, f"Error validating CSV: {str(e)}"
