"""
publisher.py — publishes the newsletter draft to Beehiiv as a draft post.
You review it there before hitting "Send".
"""

import os
import requests
from datetime import datetime


BEEHIIV_API_URL = "https://api.beehiiv.com/v2"


def publish_draft(content: str, issue_number: int = None) -> dict:
    """
    Upload newsletter as a DRAFT to Beehiiv.
    You then go to Beehiiv dashboard, review, and send manually.
    """
    api_key = os.environ["BEEHIIV_API_KEY"]
    publication_id = os.environ["BEEHIIV_PUBLICATION_ID"]

    week = datetime.now().strftime("%B %d, %Y")
    subject = f"The Pulse — Week of {week}"
    if issue_number:
        subject = f"The Pulse #{issue_number} — Week of {week}"

    # Convert markdown-ish content to simple HTML for Beehiiv
    html_content = _markdown_to_html(content)

    payload = {
        "subject": subject,
        "content": {
            "free": html_content,          # visible to all subscribers
            "premium": "",                  # premium-only section (add if needed)
        },
        "status": "draft",                  # DRAFT — you review before sending
        "audience": "free",
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
    """Very basic markdown → HTML for Beehiiv."""
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
            # Handle inline bold **text**
            processed = _inline_bold(line)
            html_lines.append(f"<p>{processed}</p>")

    return "\n".join(html_lines)


def _inline_bold(text: str) -> str:
    """Replace **text** with <strong>text</strong>."""
    import re
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
