import sqlite3
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
        cursor.execute('''
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
        ''')
        
        # Dimension: Stock
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_stock (
                stock_key INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT UNIQUE,
                company_name TEXT,
                sector TEXT,
                industry TEXT
            )
        ''')
        
        # Fact: Stock Prices
        cursor.execute('''
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
        ''')
        
        self.conn.commit()
    
    def populate_date_dimension(self, start_date, end_date):
        """Populate date dimension table"""
        cursor = self.conn.cursor()
        
        current = start_date
        while current <= end_date:
            date_key = int(current.strftime('%Y%m%d'))
            cursor.execute('''
                INSERT OR IGNORE INTO dim_date 
                (date_key, date, year, month, day, quarter, day_of_week, week_of_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
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
        cursor.execute('''
            INSERT OR IGNORE INTO dim_stock (symbol, company_name, sector, industry)
            VALUES (?, ?, ?, ?)
        ''', (symbol.upper(), company_name, sector, industry))
        self.conn.commit()
        return self.get_stock_by_symbol(symbol)
    
    def insert_stock_price(self, date_key, stock_key, open_p, high, low, close, adj_close, volume):
        """Insert a single stock price fact"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO fact_stock_prices 
            (date_key, stock_key, open_price, high_price, low_price, 
             close_price, adj_close_price, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date_key, stock_key, open_p, high, low, close, adj_close, volume))
        self.conn.commit()
    
    def get_stock_analytics(self, symbol, days=90):
        """Get analytics for a specific stock"""
        cursor = self.conn.cursor()
        
        query = '''
            SELECT d.date, f.close_price, f.volume
            FROM fact_stock_prices f
            JOIN dim_date d ON f.date_key = d.date_key
            JOIN dim_stock s ON f.stock_key = s.stock_key
            WHERE s.symbol = ?
            ORDER BY d.date DESC
            LIMIT ?
        '''
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
