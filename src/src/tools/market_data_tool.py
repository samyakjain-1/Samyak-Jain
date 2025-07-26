from ..services import market_data_service

def search_market_data(symbol: str) -> dict:
    """
    A tool that allows an agent to search for real-time and historical
    market data for a given stock symbol.

    Args:
        symbol: The stock symbol (e.g., "AAPL", "GOOG").

    Returns:
        A dictionary containing market data or an error message.
    """
    print(f"Tool 'search_market_data' called with symbol: {symbol}")
    return market_data_service.get_market_data(symbol=symbol)
