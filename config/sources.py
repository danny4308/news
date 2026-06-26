"""
RSS sources by category.
Add or remove sources here freely.
"""

SOURCES = {
    "AI & Tech": [
        "https://feeds.feedburner.com/TechCrunch",
        "https://www.technologyreview.com/feed/",
        "https://www.wired.com/feed/rss",
        "https://venturebeat.com/feed/",
    ],
    "Crypto": [
        "https://coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss",
        "https://decrypt.co/feed",
    ],
    "Science & Biotech": [
        "https://www.nature.com/nature.rss",
        "https://www.sciencedaily.com/rss/top/science.xml",
        "https://singularityhub.com/feed/",
    ],
    "Space": [
        "https://spacenews.com/feed/",
        "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "https://www.space.com/feeds/all",
    ],
    "Business & Finance": [
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://www.ft.com/rss/home",
        "https://feeds.reuters.com/reuters/businessNews",
    ],
}

# How many articles to pull per source
MAX_ARTICLES_PER_SOURCE = 10

# Only articles from the last N days
DAYS_LOOKBACK = 7
