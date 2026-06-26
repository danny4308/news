"""
writer.py — sends articles to Claude, gets back a structured newsletter draft.
"""

import json
import anthropic


SYSTEM_PROMPT = """You are the editor of "The Pulse" — a weekly newsletter for curious, intelligent people worldwide.
Your readers follow technology, crypto, biotech, space, and global business.
They are smart but not specialists. They want to understand WHY things matter, not just what happened.

Your writing style:
- Clear, direct, no fluff
- Every fact has context: "so what does this mean?"
- Honest about uncertainty
- Never hype, never doom — balanced signal
- Write in English
"""

WRITER_PROMPT_TEMPLATE = """Here are this week's news articles (JSON):

{articles_json}

Create a complete newsletter issue with this exact structure:

---
## 🔍 STORY OF THE WEEK
[Pick the single most important/interesting story. Write 150-200 words:
- What happened (2-3 sentences)
- Why it matters (2-3 sentences)  
- What comes next (1-2 sentences)]

**Source:** [publication name] | [link]

---
## ⚡ 5 BREAKTHROUGHS THIS WEEK

For each: pick the 5 most significant stories across all categories.

**1. [Headline — make it punchy]** `[CATEGORY]`
[Fact in 1 sentence]. [Why it matters in 1 sentence]. [What to watch in 1 sentence].
🔗 [link]

**2. [Headline]** `[CATEGORY]`
...

**3. [Headline]** `[CATEGORY]`
...

**4. [Headline]** `[CATEGORY]`
...

**5. [Headline]** `[CATEGORY]`
...

---
## 📊 NUMBER OF THE WEEK
**[The number]** — [What this number is about, why it's surprising or important. 2-3 sentences max.]

---
## 💡 WHAT THIS MEANS FOR YOU
[3-4 sentences connecting this week's themes to something practical or meaningful for the average intelligent person. No finance advice. Just perspective.]

---
## 🗓️ WHAT TO WATCH NEXT WEEK
- [Upcoming event/announcement 1]
- [Upcoming event/announcement 2]
- [Upcoming event/announcement 3]

---
Return ONLY the newsletter content above. No preamble, no meta-commentary."""


def generate_newsletter(articles: list[dict]) -> str:
    """Send articles to Claude and return the newsletter draft."""
    client = anthropic.Anthropic()

    # Trim articles to avoid huge context — keep top 40
    trimmed = articles[:40]
    articles_json = json.dumps(trimmed, ensure_ascii=False, indent=2)

    print(f"Sending {len(trimmed)} articles to Claude...")

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": WRITER_PROMPT_TEMPLATE.format(articles_json=articles_json),
            }
        ],
    )

    draft = message.content[0].text
    print(f"Draft generated: {len(draft)} characters")
    return draft
