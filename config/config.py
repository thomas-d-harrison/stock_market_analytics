import os

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
