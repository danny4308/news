# The Pulse — Newsletter Agent

An AI-powered weekly newsletter that automatically collects, filters, and writes a tech/crypto/science digest.

## How it works

```
RSS Feeds → Collector → Claude AI → Draft → Beehiiv (→ You review → Send)
```

Every Sunday at 9:00 AM UTC, GitHub Actions runs the agent automatically.

---

## Setup (one time, ~30 minutes)

### 1. Fork / clone this repo to GitHub

Go to GitHub → New repository → upload these files.

### 2. Get your API keys

**Anthropic (Claude):**
- Go to https://console.anthropic.com
- Create an account → API Keys → Create Key
- Copy the key (starts with `sk-ant-...`)

**Beehiiv:**
- Go to https://beehiiv.com → Create publication
- Settings → API → Generate API Key
- Also copy your Publication ID from Settings → Publication Details

### 3. Add secrets to GitHub

In your GitHub repo → Settings → Secrets and variables → Actions → New repository secret:

| Secret name              | Value                        |
|--------------------------|------------------------------|
| `ANTHROPIC_API_KEY`      | your Claude API key          |
| `BEEHIIV_API_KEY`        | your Beehiiv API key         |
| `BEEHIIV_PUBLICATION_ID` | your Beehiiv publication ID  |

### 4. That's it!

Every Sunday the agent will:
1. Collect articles from 15+ sources
2. Generate a formatted newsletter draft
3. Push it to Beehiiv as a **draft** (not sent yet)
4. You get an email from Beehiiv → review → click Send

---

## Run locally (for testing)

```bash
# Install dependencies
pip install -r requirements.txt

# Set env vars (Mac/Linux)
export ANTHROPIC_API_KEY=sk-ant-...
export BEEHIIV_API_KEY=your_key
export BEEHIIV_PUBLICATION_ID=your_pub_id

# Run without publishing (just saves draft locally)
python main.py

# Run and push to Beehiiv
python main.py --publish

# With issue number
python main.py --publish --issue 1
```

Draft is saved to `drafts/draft_YYYY-MM-DD.md`

---

## Customize sources

Edit `config/sources.py` to add/remove RSS feeds per category.

## Customize the newsletter format

Edit the `WRITER_PROMPT_TEMPLATE` in `src/writer.py`.

---

## Cost estimate

- Claude API: ~$2–5 per weekly issue (using claude-opus-4-6)
- Beehiiv: Free up to 2,500 subscribers
- GitHub Actions: Free (well within free tier limits)

**Monthly cost: ~$10–20**
