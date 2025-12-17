import unittest
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
