import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

class StockDataLoader:
    def __init__(self, warehouse):
        self.warehouse = warehouse
    
    def add_stock_with_data(self, symbol, days=180):
        """Add stock and load historical data"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Add to dimension table
            stock_key = self.warehouse.add_stock(
                symbol=symbol.upper(),
                company_name=info.get('longName', symbol),
                sector=info.get('sector', 'Unknown'),
                industry=info.get('industry', 'Unknown')
            )
            
            if not stock_key:
                return False, "Could not add stock to database"
            
            # Download historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            df = yf.download(symbol, start=start_date, end=end_date, progress=False)
            
            if df.empty:
                return False, "No data available for this symbol"
            
            # Flatten multi-index columns if present
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Normalize column names
            df.columns = df.columns.str.replace(' ', '_')
            
            # Populate date dimension
            self.warehouse.populate_date_dimension(start_date, end_date)
            
            # Insert price facts
            for date, row in df.iterrows():
                date_key = int(date.strftime('%Y%m%d'))
                
                # Get adj close with fallback
                adj_close = row.get('Adj_Close', row.get('Close', 0))
                
                self.warehouse.insert_stock_price(
                    date_key, stock_key,
                    float(row['Open']), float(row['High']), float(row['Low']),
                    float(row['Close']), float(adj_close), int(row['Volume'])
                )
            
            return True, "Stock data loaded successfully"
            
        except Exception as e:
            return False, f"Error: {str(e)}"