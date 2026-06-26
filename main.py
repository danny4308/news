"""
main.py — orchestrates the full pipeline:
  1. Collect articles from RSS feeds
  2. Generate newsletter draft via Claude
  3. Save draft locally
  4. (Optional) Publish to Beehiiv

Run locally:   python main.py
Run with push: python main.py --publish
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Make src/ importable
sys.path.insert(0, str(Path(__file__).parent))

from src.collector import fetch_all_articles
from src.writer import generate_newsletter
from src.publisher import publish_draft


def main():
    parser = argparse.ArgumentParser(description="The Pulse — Newsletter Agent")
    parser.add_argument("--publish", action="store_true", help="Publish draft to Beehiiv")
    parser.add_argument("--issue", type=int, default=None, help="Issue number")
    args = parser.parse_args()

    print("=" * 50)
    print("THE PULSE — Newsletter Agent")
    print("=" * 50)

    # Step 1: Collect
    print("\n📡 Step 1: Collecting articles...")
    articles = fetch_all_articles()

    if not articles:
        print("No articles found. Check your RSS sources.")
        sys.exit(1)

    # Step 2: Generate
    print("\n✍️  Step 2: Generating newsletter draft...")
    draft = generate_newsletter(articles)

    # Step 3: Save locally
    output_dir = Path("drafts")
    output_dir.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = output_dir / f"draft_{date_str}.md"
    output_path.write_text(draft, encoding="utf-8")
    print(f"\n💾 Draft saved to: {output_path}")

    # Step 4: Publish (optional)
    if args.publish:
        print("\n🚀 Step 3: Publishing to Beehiiv...")
        result = publish_draft(draft, issue_number=args.issue)
        print(f"   Post ID : {result['id']}")
        print(f"   URL     : {result['url']}")
    else:
        print("\n💡 Tip: run with --publish to push draft to Beehiiv")

    print("\n✅ Done! Review your draft before sending.")
    print("=" * 50)


if __name__ == "__main__":
    main()
