"""
publisher.py — publishes the newsletter draft to Beehiiv as a draft post.
"""

import os
import re
import requests
from datetime import datetime


BEEHIIV_API_URL = "https://api.beehiiv.com/v2"


def publish_draft(content: str, issue_number: int = None) -> dict:
    api_key = os.environ["BEEHIIV_API_KEY"]
    publication_id = os.environ["BEEHIIV_PUBLICATION_ID"]

    week = datetime.now().strftime("%B %d, %Y")
    title = f"The Pulse — Week of {week}"
    if issue_number:
        title = f"The Pulse #{issue_number} — Week of {week}"

    html_content = _markdown_to_html(content)

    payload = {
        "subject": title,
        "title": title,
        "body_content": html_content,
        "status": "draft",
    }

    resp = requests.post(
        f"{BEEHIIV_API_URL}/publications/{publication_id}/posts",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

    resp.raise_for_status()
    data = resp.json()
    post_url = data.get("data", {}).get("url", "—")
    post_id = data.get("data", {}).get("id", "—")
    print(f"✓ Draft created on Beehiiv: {post_url}")
    return {"id": post_id, "url": post_url}


def _markdown_to_html(text: str) -> str:
    lines = text.split("\n")
    html_lines = []

    for line in lines:
        if line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("**") and line.endswith("**"):
            html_lines.append(f"<strong>{line[2:-2]}</strong>")
        elif line.startswith("- "):
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.startswith("---"):
            html_lines.append("<hr>")
        elif line.strip() == "":
            html_lines.append("<br>")
        else:
            processed = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            html_lines.append(f"<p>{processed}</p>")

    return "\n".join(html_lines)
