#!/usr/bin/env python
"""Initialize the database with schema"""

import sys
import os

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import StockDataWarehouse
from config.config import Config

def main():
    print("Initializing Stock Analytics Database...")
    print(f"Database location: {Config.DATABASE_PATH}")
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Create warehouse (this creates the schema)
    warehouse = StockDataWarehouse(Config.DATABASE_PATH)
    
    print("✓ Star schema created successfully!")
    print("\nTables created:")
    print("  - dim_date (Date dimension)")
    print("  - dim_stock (Stock dimension)")
    print("  - fact_stock_prices (Price facts)")
    
    warehouse.close()
    print("\nDatabase ready! Run 'python -m src.web.app' to start the web server.")

if __name__ == '__main__':
    main()
