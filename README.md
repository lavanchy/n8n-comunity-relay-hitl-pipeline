# Relay HITL Content Pipeline

n8n Community Challenge — Human-in-the-Loop content pipeline for social media post creation.

Built for **Relay**, a content agency. Demo client: **Loopin** (async video tool for remote teams).

**Deadline:** 25. Mai 2026

---

## What it does

Takes a content brief (client, platform, topic, tone) through three AI-reviewed stages:

1. **Sofia** — generates 3 content angle options → human picks one
2. **Marcus** — writes post copy + image direction → human reviews (with AI preview of what Taylor will say)
3. **Taylor** — final quality check → human approves or sends back

Final approved posts are logged to Google Sheets.

```
Form → Sofia AI → Sofia Review → Marcus AI → Taylor Preview → Marcus Review → Taylor AI → Taylor Review → Google Sheets
```

---

## Key feature: Marcus Preview Loop

Before Marcus's gotoHuman review, a Claude API call simulates Taylor's QC perspective and returns a structured JSON summary with quality flags. Marcus sees this in his review form and can self-correct before Taylor sees the post. This reduces revision loops between Marcus and Taylor.

---

## Repo structure

```
workflows/
  relay-hitl-pipeline.json    ← n8n workflow (import this)
resources/
  loopin-brand-guide.md       ← client brand context
  relay-platform-playbook.md  ← platform specs (LinkedIn, X, Instagram)
test-briefs/
  TB-01-linkedin-product.md   ← Easy: happy path test
  TB-02-x-thought-leadership.md ← Medium: Sofia revision loop test
  TB-03-linkedin-customer-story.md
  TB-04-instagram-culture.md  ← Hard: Marcus preview loop test
  TB-05-linkedin-data-post.md
prompts/
  sofia-system-prompt.md
  marcus-system-prompt.md
  taylor-preview-prompt.md    ← Claude API call (JSON output only)
  taylor-system-prompt.md
docs/
  architecture.md             ← Full workflow diagram + stage details
  gotohuman-setup.md          ← gotoHuman template setup guide
```

---

## Setup

### 1. n8n

```bash
cp .env.example .env
# Fill in N8N_API_KEY
```

Import `workflows/relay-hitl-pipeline.json` into n8n.

### 2. Credentials needed in n8n

| Credential | Notes |
|---|---|
| Anthropic | Already on VPS as credential `iwvg3egDYZxTmjDy` |
| gotoHuman | Install community node `n8n-nodes-gotohuman` first |
| Google Sheets | OAuth2, create in n8n credentials |

### 3. gotoHuman

Follow [docs/gotohuman-setup.md](docs/gotohuman-setup.md):
- Create 3 review templates (Sofia, Marcus, Taylor)
- Add API key to `.env` as `GOTOHUMAN_API_KEY`

### 4. Google Sheets

Create a sheet with columns matching the output schema in [docs/architecture.md](docs/architecture.md#google-sheets-output-schema).
Add the spreadsheet ID to `.env`.

---

## Testing

Run the three demo scenarios:

| Brief | Scenario | What to show |
|---|---|---|
| [TB-01](test-briefs/TB-01-linkedin-product.md) | Happy path | All stages approve on first try, post logged to Sheets |
| [TB-02](test-briefs/TB-02-x-thought-leadership.md) | Sofia revision loop | First angles are too generic, reviewer sends back, second attempt is Loopin-specific |
| [TB-04](test-briefs/TB-04-instagram-culture.md) | Marcus preview loop | Taylor preview flags vague visual, Marcus self-corrects before Taylor review |

---

## References

- [Workflow Architecture](docs/architecture.md)
- [gotoHuman Setup](docs/gotohuman-setup.md)
- [Loopin Brand Guide](resources/loopin-brand-guide.md)
- [Relay Platform Playbook](resources/relay-platform-playbook.md)
