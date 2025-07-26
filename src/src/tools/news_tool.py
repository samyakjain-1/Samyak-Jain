from ..services import news_service

def search_news(query: str, days: int = 7) -> dict:
    """
    A tool that allows an agent to search for financial news.

    Args:
        query: The search term (e.g., a company name or stock symbol).
        days: The number of past days to search within.

    Returns:
        A dictionary containing a list of articles or an error message.
    """
    print(f"Tool 'search_news' called with query: {query}")
    return news_service.get_news(query=query, days=days)
