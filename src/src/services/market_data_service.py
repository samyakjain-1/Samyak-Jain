import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MarketDataService:
    def __init__(self):
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.fmp_key = os.getenv("FMP_API_KEY")
        self._cache = {}
        self._cache_duration = 300  # 5 minutes

    def get_stock_data(self, symbol):
        if not symbol:
            return {'error': 'Invalid symbol'}
        
        symbol = symbol.upper().strip()
        cache_key = f"{symbol}_{int(time.time() // self._cache_duration)}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Try Alpha Vantage
        if self.alpha_vantage_key:
            try:
                data = self._fetch_alpha_vantage(symbol)
                self._cache[cache_key] = data
                return data
            except Exception as e:
                print(f"Alpha Vantage failed for {symbol}: {e}")

        # Try FMP
        if self.fmp_key:
            try:
                data = self._fetch_fmp(symbol)
                self._cache[cache_key] = data
                return data
            except Exception as e:
                print(f"FMP failed for {symbol}: {e}")

        # Fallback to Yahoo Finance
        try:
            data = self._fetch_yahoo(symbol)
            self._cache[cache_key] = data
            return data
        except Exception as e:
            print(f"Yahoo Finance failed for {symbol}: {e}")
            return {'error': f'All data sources failed for {symbol}'}

    def _fetch_alpha_vantage(self, symbol):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.alpha_vantage_key}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if 'Global Quote' not in data or not data['Global Quote']:
            raise ValueError("Invalid symbol or no data from Alpha Vantage")
        
        quote = data['Global Quote']
        price = float(quote.get('05. price', 0))
        if price <= 0:
            raise ValueError("Invalid price data from Alpha Vantage")
            
        return {
            'source': 'alpha_vantage',
            'symbol': symbol,
            'price': price,
            'previous_close': float(quote.get('08. previous close', 0)),
            'change': float(quote.get('09. change', 0)),
            'change_percent': float(quote.get('10. change percent', '0%').replace('%', '')),
            'volume': int(quote.get('06. volume', 0))
        }

    def _fetch_fmp(self, symbol):
        url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={self.fmp_key}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError("Invalid symbol or no data from FMP")
            
        quote = data[0]
        price = float(quote.get('price', 0))
        if price <= 0:
            raise ValueError("Invalid price data from FMP")

        return {
            'source': 'fmp',
            'symbol': symbol,
            'price': price,
            'previous_close': float(quote.get('previousClose', 0)),
            'change': float(quote.get('change', 0)),
            'change_percent': float(quote.get('changesPercentage', 0)),
            'volume': int(quote.get('volume', 0)),
            'market_cap': int(quote.get('marketCap', 0))
        }

    def _fetch_yahoo(self, symbol):
        from bs4 import BeautifulSoup
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = f"https://finance.yahoo.com/quote/{symbol}"
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        price_element = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
        if not price_element:
            raise ValueError("Could not find price element on Yahoo Finance page")
            
        price = float(price_element.get('value', 0))
        if price <= 0:
            raise ValueError("Invalid price data from Yahoo Finance")

        return {
            'source': 'yahoo_scraped',
            'symbol': symbol,
            'price': price
        }

# Singleton instance
market_data_service = MarketDataService()

def get_market_data(symbol: str) -> dict:
    return market_data_service.get_stock_data(symbol)
