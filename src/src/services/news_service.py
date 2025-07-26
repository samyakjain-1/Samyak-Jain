import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def get_news(query: str, days: int = 7) -> dict:
    """
    Service for retrieving financial news from Alpha Vantage.
    """
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return {"error": "ALPHA_VANTAGE_API_KEY not found in environment variables."}

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={query}&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'feed' not in data:
            return {"error": "No news data found in API response.", "response": data}

        # Filter for recent news
        cutoff_date = datetime.now() - timedelta(days=days)
        
        processed_articles = []
        for article in data['feed']:
            try:
                # Alpha Vantage time format is YYYYMMDD'T'HHMMSS
                published_time = datetime.strptime(article.get('time_published', ''), '%Y%m%dT%H%M%S')
                if published_time >= cutoff_date:
                    processed_articles.append({
                        "title": article.get('title', ''),
                        "summary": article.get('summary', ''),
                        "source": article.get('source', ''),
                        "url": article.get('url', ''),
                        "published": published_time.isoformat(),
                        "sentiment_score": article.get('overall_sentiment_score', 0),
                        "sentiment_label": article.get('overall_sentiment_label', 'Neutral')
                    })
            except (ValueError, TypeError):
                # Skip articles with invalid date formats
                continue
        
        # Limit to the 20 most recent articles
        return {
            "query": query,
            "articles": processed_articles[:20],
            "status": "success"
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}", "status": "error"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}", "status": "error"}
