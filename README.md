# 📈 Stock Market Analytics System

>A data warehouse system using star schema design for analyzing stock market data with real-time fetching from Yahoo Finance.


![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![SQLite](https://img.shields.io/badge/sqlite-3-yellow.svg)


## 🐍 Prerequisites

**Python 3.8+** is required. Don't have Python? 

[![](https://img.shields.io/badge/Download-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)

## Features

- ⭐ Star schema data design
- 📊 Real-time market data
- 🌐 Interactive web interface
- 📉 Visual analytics with Plotly 
- 💾 SQLite database for persistent storage

## 📂 Project Structure
```
stock-analytics/
├── 📊 src/                     # Source code
│   ├── 🗄️ database/
│   │   ├── __init__.py
│   │   └── warehouse.py        # Star schema & data warehouse logic
│   ├── 📥 data/
│   │   ├── __init__.py
│   │   └── loader.py           # Yahoo Finance ETL processes
│   └── 🌐 web/
│       ├── __init__.py
│       ├── app.py              # Flask application
│       └── templates/
│           └── index.html      # Dashboard UI
├── 🧪 tests/                   # Unit tests
│   ├── __init__.py
│   └── test_warehouse.py
├── ⚙️ scripts/                 # Utility scripts
│   └── initialize_db.py        # Database initialization
├── 🔧 config/                  # Configuration
│   ├── __init__.py
│   └── config.py               # App settings
├── 💾 data/                    # Database storage
│   └── stock_warehouse.db      # SQLite database (gitignored)
├── 📄 requirements.txt         # Python dependencies
├── 📝 README.md
└── ⚙️ setup.py
```

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
```mermaid
erDiagram
    fact_stock_prices ||--o{ dim_date : "date_key"
    fact_stock_prices ||--o{ dim_stock : "stock_key"
    
    dim_date {
        int date_key PK
        text date
        int year
        int month
        int day
        int quarter
        int day_of_week
        int week_of_year
    }
    
    dim_stock {
        int stock_key PK
        text symbol
        text company_name
        text sector
        text industry
    }
    
    fact_stock_prices {
        int fact_key PK
        int date_key FK
        int stock_key FK
        real open_price
        real high_price
        real low_price
        real close_price
        real adj_close_price
        int volume
    }
```

**Fact Table:**
- `fact_stock_prices` - Daily stock price data

**Dimension Tables:**
- `dim_date` - Date dimensions (year, month, quarter, week)
- `dim_stock` - Stock information (symbol, company, sector, industry)

## 🛠️ Tech Stack

- **Backend:** Python, SQLite
- **Frontend:** HTML, CSS, JavaScript

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📝 License

MIT License

Copyright (c) 2025 Thomas Harrison

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


