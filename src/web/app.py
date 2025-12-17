from flask import Flask, render_template, jsonify, request
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
    print(f"\nWeb interface: http://{Config.FLASK_HOST}:{Config.FLASK_PORT}")
    print("\nTry adding: AAPL, GOOGL, MSFT, TSLA")
    print("="*60)
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
