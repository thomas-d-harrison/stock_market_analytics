#!/usr/bin/env python3
"""
Project Structure Builder for Stock Analytics System
Run this script to automatically create all folders and files for the project.
"""

import os
import sys

# Project structure with file contents
PROJECT_STRUCTURE = {
    'requirements.txt': '''yfinance
pandas
flask
plotly
''',

    '.gitignore': '''# Database files
*.db
*.sqlite
*.sqlite3

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment variables
.env
''',

    'README.md': '''# 📈 Stock Market Analytics System

A data warehouse system using star schema design for analyzing stock market data with real-time fetching from Yahoo Finance.

## Features

- ⭐ Star schema database design (fact & dimension tables)
- 📊 Real-time stock data from Yahoo Finance
- 🌐 Interactive web interface
- 📉 Visual analytics with Plotly charts
- 💾 SQLite database for persistent storage

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   venv\\Scripts\\activate
   ```
   > **Mac/Linux:** Use `source venv/bin/activate` instead

4. **Upgrade pip and install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install --only-binary :all: numpy pandas
   pip install -r requirements.txt
   ```
   > **Mac/Linux:** You can skip the `--only-binary` command and just run `pip install -r requirements.txt`

5. **Initialize the database:**
   ```bash
   python -m scripts.initialize_db
   ```

## Usage

1. Start the web server:
   ```bash
   python -m src.web.app
   ```

2. Open your browser to `http://127.0.0.1:5000`

3. Add stocks using their ticker symbols (AAPL, GOOGL, MSFT, etc.)

4. Click on any stock to view detailed analytics

## Database Schema

### Star Schema Design

**Fact Table:**
- `fact_stock_prices` - Daily stock price data

**Dimension Tables:**
- `dim_date` - Date dimensions (year, month, quarter, week)
- `dim_stock` - Stock information (symbol, company, sector, industry)

## Project Structure

- `src/database/` - Database models and warehouse logic
- `src/data/` - Data loading and ETL processes
- `src/web/` - Flask web application
- `tests/` - Unit tests
- `scripts/` - Utility scripts
- `config/` - Configuration files

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## License

MIT
''',

    'SETUP_INSTRUCTIONS.txt': '''========================================
Stock Analytics - Setup Instructions
========================================

WINDOWS USERS:
--------------
1. Open Command Prompt or PowerShell in this directory
2. Run: python -m venv venv
3. Run: venv\\Scripts\\activate
4. Run: pip install --upgrade pip
5. Run: pip install --only-binary :all: numpy pandas
6. Run: pip install -r requirements.txt
7. Run: python scripts\\initialize_db.py
8. Run: python -m src.web.app
9. Open browser to: http://127.0.0.1:5000

MAC/LINUX USERS:
----------------
1. Open Terminal in this directory
2. Run: python3 -m venv venv
3. Run: source venv/bin/activate
4. Run: pip install --upgrade pip
5. Run: pip install -r requirements.txt
6. Run: python scripts/initialize_db.py
7. Run: python -m src.web.app
8. Open browser to: http://127.0.0.1:5000

TROUBLESHOOTING:
----------------
If you get compiler errors on Windows:
- Make sure to use: pip install --only-binary :all: numpy pandas
- This forces pip to use prebuilt wheels instead of compiling

If imports fail:
- Make sure you're in the project root directory
- Make sure virtual environment is activated
- Try: pip install -e .
''',

    'setup.py': '''from setuptools import setup, find_packages

setup(
    name="stock-analytics",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "yfinance",
        "pandas",
        "flask",
        "plotly",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Stock market analytics with star schema data warehouse",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/stock-analytics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
''',

    'config/__init__.py': '"""Configuration module"""',

    'config/config.py': '''import os

class Config:
    # Database
    DATABASE_NAME = os.getenv('DB_NAME', 'stock_warehouse.db')
    DATABASE_PATH = os.path.join('data', DATABASE_NAME)
    
    # Flask
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Data loading
    DEFAULT_HISTORY_DAYS = 180
    CHART_DISPLAY_DAYS = 90
''',

    'src/__init__.py': '''"""Stock Market Analytics System"""
__version__ = "1.0.0"
''',

    'src/database/__init__.py': '''from .warehouse import StockDataWarehouse

__all__ = ['StockDataWarehouse']
''',

    'src/database/warehouse.py': '''import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

class StockDataWarehouse:
    def __init__(self, db_path='data/stock_warehouse.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = None
        self.create_star_schema()
    
    def create_star_schema(self):
        """Create star schema with fact and dimension tables"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Dimension: Date
        cursor.execute(\'\'\'
            CREATE TABLE IF NOT EXISTS dim_date (
                date_key INTEGER PRIMARY KEY,
                date TEXT UNIQUE,
                year INTEGER,
                month INTEGER,
                day INTEGER,
                quarter INTEGER,
                day_of_week INTEGER,
                week_of_year INTEGER
            )
        \'\'\')
        
        # Dimension: Stock
        cursor.execute(\'\'\'
            CREATE TABLE IF NOT EXISTS dim_stock (
                stock_key INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT UNIQUE,
                company_name TEXT,
                sector TEXT,
                industry TEXT
            )
        \'\'\')
        
        # Fact: Stock Prices
        cursor.execute(\'\'\'
            CREATE TABLE IF NOT EXISTS fact_stock_prices (
                fact_key INTEGER PRIMARY KEY AUTOINCREMENT,
                date_key INTEGER,
                stock_key INTEGER,
                open_price REAL,
                high_price REAL,
                low_price REAL,
                close_price REAL,
                adj_close_price REAL,
                volume INTEGER,
                FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
                FOREIGN KEY (stock_key) REFERENCES dim_stock(stock_key)
            )
        \'\'\')
        
        self.conn.commit()
    
    def populate_date_dimension(self, start_date, end_date):
        """Populate date dimension table"""
        cursor = self.conn.cursor()
        
        current = start_date
        while current <= end_date:
            date_key = int(current.strftime('%Y%m%d'))
            cursor.execute(\'\'\'
                INSERT OR IGNORE INTO dim_date 
                (date_key, date, year, month, day, quarter, day_of_week, week_of_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            \'\'\', (
                date_key,
                current.strftime('%Y-%m-%d'),
                current.year,
                current.month,
                current.day,
                (current.month - 1) // 3 + 1,
                current.weekday(),
                current.isocalendar()[1]
            ))
            current += timedelta(days=1)
        
        self.conn.commit()
    
    def get_stock_by_symbol(self, symbol):
        """Get stock_key for a symbol"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT stock_key FROM dim_stock WHERE symbol = ?', (symbol.upper(),))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def add_stock(self, symbol, company_name, sector='Unknown', industry='Unknown'):
        """Add stock to dimension table"""
        cursor = self.conn.cursor()
        cursor.execute(\'\'\'
            INSERT OR IGNORE INTO dim_stock (symbol, company_name, sector, industry)
            VALUES (?, ?, ?, ?)
        \'\'\', (symbol.upper(), company_name, sector, industry))
        self.conn.commit()
        return self.get_stock_by_symbol(symbol)
    
    def insert_stock_price(self, date_key, stock_key, open_p, high, low, close, adj_close, volume):
        """Insert a single stock price fact"""
        cursor = self.conn.cursor()
        cursor.execute(\'\'\'
            INSERT OR REPLACE INTO fact_stock_prices 
            (date_key, stock_key, open_price, high_price, low_price, 
             close_price, adj_close_price, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        \'\'\', (date_key, stock_key, open_p, high, low, close, adj_close, volume))
        self.conn.commit()
    
    def get_stock_analytics(self, symbol, days=90):
        """Get analytics for a specific stock"""
        cursor = self.conn.cursor()
        
        query = \'\'\'
            SELECT d.date, f.close_price, f.volume
            FROM fact_stock_prices f
            JOIN dim_date d ON f.date_key = d.date_key
            JOIN dim_stock s ON f.stock_key = s.stock_key
            WHERE s.symbol = ?
            ORDER BY d.date DESC
            LIMIT ?
        \'\'\'
        cursor.execute(query, (symbol.upper(), days))
        data = cursor.fetchall()
        
        if not data:
            return None
        
        df = pd.DataFrame(data, columns=['date', 'close_price', 'volume'])
        df = df.sort_values('date')
        
        current_price = df['close_price'].iloc[-1]
        prev_price = df['close_price'].iloc[-2] if len(df) > 1 else current_price
        price_change = current_price - prev_price
        price_change_pct = (price_change / prev_price * 100) if prev_price != 0 else 0
        
        return {
            'symbol': symbol.upper(),
            'current_price': round(current_price, 2),
            'price_change': round(price_change, 2),
            'price_change_pct': round(price_change_pct, 2),
            'high': round(df['close_price'].max(), 2),
            'low': round(df['close_price'].min(), 2),
            'avg_volume': int(df['volume'].mean()),
            'chart_data': df.to_dict('records')
        }
    
    def get_all_stocks(self):
        """Get list of all stocks in database"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT symbol, company_name, sector FROM dim_stock')
        return cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
''',

    'src/data/__init__.py': '''from .loader import StockDataLoader

__all__ = ['StockDataLoader']
''',

    'src/data/loader.py': '''import yfinance as yf
from datetime import datetime, timedelta

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
            
            # Normalize column names (handle both 'Adj Close' and 'Adj_Close')
            df.columns = df.columns.str.replace(' ', '_')
            
            # Populate date dimension
            self.warehouse.populate_date_dimension(start_date, end_date)
            
            # Insert price facts - handle different possible column names
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
''',

    'src/web/__init__.py': '''from .app import create_app

__all__ = ['create_app']
''',

    'src/web/app.py': '''from flask import Flask, render_template, jsonify, request
from src.database import StockDataWarehouse
from src.data import StockDataLoader
from config.config import Config

def create_app(config=None):
    app = Flask(__name__, template_folder='templates')
    
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(Config)
    
    warehouse = StockDataWarehouse(app.config['DATABASE_PATH'])
    loader = StockDataLoader(warehouse)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/add_stock', methods=['POST'])
    def add_stock():
        data = request.json
        symbol = data.get('symbol', '').upper()
        
        if not symbol:
            return jsonify({'success': False, 'message': 'No symbol provided'})
        
        success, message = loader.add_stock_with_data(symbol)
        return jsonify({'success': success, 'message': message})
    
    @app.route('/stocks')
    def get_stocks():
        stocks = warehouse.get_all_stocks()
        return jsonify({'stocks': stocks})
    
    @app.route('/analytics/<symbol>')
    def get_analytics(symbol):
        analytics = warehouse.get_stock_analytics(symbol)
        if analytics:
            return jsonify(analytics)
        return jsonify({'error': 'No data found'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("="*60)
    print("Stock Market Analytics System")
    print("="*60)
    print(f"\\nWeb interface: http://{Config.FLASK_HOST}:{Config.FLASK_PORT}")
    print("\\nTry adding: AAPL, GOOGL, MSFT, TSLA")
    print("="*60)
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
''',

    'src/web/templates/index.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Stock Market Analytics</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .section h2 {
            color: #667eea;
            margin-top: 0;
        }
        input, button {
            padding: 10px 15px;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #5568d3;
        }
        .stock-card {
            display: inline-block;
            margin: 10px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            min-width: 250px;
        }
        .stock-card h3 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .price {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }
        .change {
            font-size: 18px;
            margin: 10px 0;
        }
        .positive { color: #28a745; }
        .negative { color: #dc3545; }
        .metric {
            margin: 5px 0;
            color: #666;
        }
        #chart {
            margin-top: 20px;
            height: 400px;
        }
        .stock-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .stock-item {
            padding: 15px;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .stock-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 Stock Market Analytics System</h1>
        
        <div class="section">
            <h2>Add New Stock</h2>
            <input type="text" id="symbolInput" placeholder="Stock Symbol (e.g., AAPL)" />
            <button onclick="addStock()">Add Stock</button>
            <div id="addMessage" style="margin-top: 10px;"></div>
        </div>
        
        <div class="section">
            <h2>Available Stocks</h2>
            <div id="stockList" class="stock-list"></div>
        </div>
        
        <div class="section" id="analyticsSection" style="display: none;">
            <h2>Stock Analytics</h2>
            <div id="stockCard"></div>
            <div id="chart"></div>
        </div>
    </div>

    <script>
        function addStock() {
            const symbol = document.getElementById('symbolInput').value.toUpperCase();
            const msg = document.getElementById('addMessage');
            
            if (!symbol) {
                msg.innerHTML = '<span style="color: red;">Please enter a symbol</span>';
                return;
            }
            
            msg.innerHTML = '<span style="color: blue;">Adding stock and downloading data...</span>';
            
            fetch('/add_stock', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({symbol: symbol})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    msg.innerHTML = '<span style="color: green;">✓ Stock added successfully!</span>';
                    document.getElementById('symbolInput').value = '';
                    loadStockList();
                } else {
                    msg.innerHTML = '<span style="color: red;">✗ ' + data.message + '</span>';
                }
            });
        }
        
        function loadStockList() {
            fetch('/stocks')
            .then(r => r.json())
            .then(data => {
                const list = document.getElementById('stockList');
                if (data.stocks.length === 0) {
                    list.innerHTML = '<p style="color: #666;">No stocks added yet. Add one above!</p>';
                } else {
                    list.innerHTML = data.stocks.map(s => `
                        <div class="stock-item" onclick="viewStock('${s[0]}')">
                            <strong>${s[0]}</strong><br>
                            <small>${s[1]}</small><br>
                            <small style="color: #666;">${s[2]}</small>
                        </div>
                    `).join('');
                }
            });
        }
        
        function viewStock(symbol) {
            fetch('/analytics/' + symbol)
            .then(r => r.json())
            .then(data => {
                if (!data.error) {
                    const section = document.getElementById('analyticsSection');
                    section.style.display = 'block';
                    
                    const changeClass = data.price_change >= 0 ? 'positive' : 'negative';
                    const changeSymbol = data.price_change >= 0 ? '▲' : '▼';
                    
                    document.getElementById('stockCard').innerHTML = `
                        <div class="stock-card">
                            <h3>${data.symbol}</h3>
                            <div class="price">$${data.current_price}</div>
                            <div class="change ${changeClass}">
                                ${changeSymbol} $${Math.abs(data.price_change)} 
                                (${data.price_change_pct}%)
                            </div>
                            <div class="metric">High: $${data.high}</div>
                            <div class="metric">Low: $${data.low}</div>
                            <div class="metric">Avg Volume: ${data.avg_volume.toLocaleString()}</div>
                        </div>
                    `;
                    
                    const dates = data.chart_data.map(d => d.date);
                    const prices = data.chart_data.map(d => d.close_price);
                    
                    Plotly.newPlot('chart', [{
                        x: dates,
                        y: prices,
                        type: 'scatter',
                        mode: 'lines',
                        line: {color: '#667eea', width: 2},
                        fill: 'tozeroy',
                        fillcolor: 'rgba(102, 126, 234, 0.1)'
                    }], {
                        title: data.symbol + ' Price History (90 Days)',
                        xaxis: {title: 'Date'},
                        yaxis: {title: 'Price ($)'},
                        margin: {t: 40, r: 40, b: 40, l: 60}
                    });
                    
                    section.scrollIntoView({behavior: 'smooth'});
                }
            });
        }
        
        loadStockList();
    </script>
</body>
</html>
''',

    'tests/__init__.py': '"""Test module"""',

    'tests/test_warehouse.py': '''import unittest
import os
from src.database import StockDataWarehouse
from datetime import datetime

class TestStockDataWarehouse(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_warehouse.db'
        self.warehouse = StockDataWarehouse(self.test_db)
    
    def tearDown(self):
        self.warehouse.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_add_stock(self):
        stock_key = self.warehouse.add_stock('AAPL', 'Apple Inc.', 'Technology', 'Consumer Electronics')
        self.assertIsNotNone(stock_key)
        
        retrieved_key = self.warehouse.get_stock_by_symbol('AAPL')
        self.assertEqual(stock_key, retrieved_key)
    
    def test_get_all_stocks(self):
        self.warehouse.add_stock('AAPL', 'Apple Inc.')
        self.warehouse.add_stock('GOOGL', 'Alphabet Inc.')
        
        stocks = self.warehouse.get_all_stocks()
        self.assertEqual(len(stocks), 2)

if __name__ == '__main__':
    unittest.main()
''',

    'scripts/initialize_db.py': '''#!/usr/bin/env python
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
    print("\\nTables created:")
    print("  - dim_date (Date dimension)")
    print("  - dim_stock (Stock dimension)")
    print("  - fact_stock_prices (Price facts)")
    
    warehouse.close()
    print("\\nDatabase ready! Run 'python -m src.web.app' to start the web server.")

if __name__ == '__main__':
    main()
''',

    'data/.gitkeep': '''# This file ensures the data directory is tracked by git
# Database files will be gitignored but the directory structure is preserved
''',
}


def create_project_structure(base_path='stock-analytics'):
    """Create the complete project structure"""
    
    print("="*70)
    print("Stock Analytics Project Structure Builder")
    print("Windows-Optimized Version")
    print("="*70)
    print()
    
    # Check if directory already exists
    if os.path.exists(base_path):
        response = input(f"Directory '{base_path}' already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    # Create base directory
    os.makedirs(base_path, exist_ok=True)
    print(f"✓ Created base directory: {base_path}\\")
    
    # Create all files and directories
    created_files = []
    created_dirs = set()
    
    for file_path, content in PROJECT_STRUCTURE.items():
        full_path = os.path.join(base_path, file_path)
        
        # Create parent directories if needed
        parent_dir = os.path.dirname(full_path)
        if parent_dir and parent_dir not in created_dirs:
            os.makedirs(parent_dir, exist_ok=True)
            created_dirs.add(parent_dir)
            print(f"✓ Created directory: {parent_dir}\\")
        
        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        created_files.append(file_path)
        print(f"  ✓ Created file: {file_path}")
    
    print()
    print("="*70)
    print("✅ Project structure created successfully!")
    print("="*70)
    print()
    print("WINDOWS SETUP - Follow these steps:")
    print()
    print(f"  1. cd {base_path}")
    print("  2. python -m venv venv")
    print("  3. venv\\Scripts\\activate")
    print("  4. pip install --upgrade pip")
    print("  5. pip install --only-binary :all: numpy pandas")
    print("  6. pip install -r requirements.txt")
    print("  7. python scripts\\initialize_db.py")
    print("  8. python -m src.web.app")
    print("  9. Open browser to: http://127.0.0.1:5000")
    print()
    print("See SETUP_INSTRUCTIONS.txt for full details")
    print()
    print(f"Total files created: {len(created_files)}")
    print(f"Total directories created: {len(created_dirs) + 1}")
    print()


if __name__ == '__main__':
    try:
        # Allow custom project name from command line
        if len(sys.argv) > 1:
            project_name = sys.argv[1]
        else:
            project_name = 'stock-analytics'
        
        create_project_structure(project_name)
        
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)