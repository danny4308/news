"""
collector.py — fetches articles from RSS feeds and returns raw data.
"""

import feedparser
import requests
from datetime import datetime, timezone, timedelta
from config.sources import SOURCES, MAX_ARTICLES_PER_SOURCE, DAYS_LOOKBACK


def fetch_all_articles() -> list[dict]:
    """Fetch articles from all RSS sources, filter by recency."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS_LOOKBACK)
    all_articles = []

    for category, feeds in SOURCES.items():
        for feed_url in feeds:
            try:
                articles = _fetch_feed(feed_url, category, cutoff)
                all_articles.extend(articles)
                print(f"  ✓ {feed_url} → {len(articles)} articles")
            except Exception as e:
                print(f"  ✗ {feed_url} → error: {e}")

    print(f"\nTotal collected: {len(all_articles)} articles")
    return all_articles


def _fetch_feed(url: str, category: str, cutoff: datetime) -> list[dict]:
    """Parse one RSS feed and return recent articles."""
    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
        # Parse publish date
        published = _parse_date(entry)
        if published and published < cutoff:
            continue  # too old

        articles.append({
            "title": entry.get("title", "").strip(),
            "summary": entry.get("summary", entry.get("description", ""))[:500],
            "link": entry.get("link", ""),
            "published": published.isoformat() if published else "unknown",
            "category": category,
            "source": feed.feed.get("title", url),
        })

    return articles


def _parse_date(entry) -> datetime | None:
    """Try to extract a timezone-aware datetime from feed entry."""
    for field in ("published_parsed", "updated_parsed"):
        t = getattr(entry, field, None)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None
