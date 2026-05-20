# gotoHuman Setup Guide

## Overview

The pipeline uses 3 gotoHuman review templates — one per stage. Each template maps to a gotoHuman form that reviewers see in the gotoHuman Agent Inbox (or via Slack notification).

**gotoHuman dashboard:** https://app.gotohuman.com

---

## Step 1: Install gotoHuman n8n Community Node

In n8n:
1. Settings → Community Nodes → Install
2. Package: `n8n-nodes-gotohuman`
3. Restart n8n if prompted

---

## Step 2: Add gotoHuman Credential

1. n8n → Credentials → New
2. Type: gotoHuman API
3. Paste API key from gotoHuman → Settings → API Keys
4. Note the credential ID for `.env`

---

## Step 3: Create 3 Review Templates

### Template IDs (bereits erstellt)

| Template | ID |
|---|---|
| Sofia Review | `wOkoABOpHs7PUkBmSHJB` |
| Marcus Review | `W2o71eTDvvStzR7UBni6` |
| Taylor Review | `tjekU1jyCHgH0cbaU5UO` |

---

### Template 1: Sofia Review (`wOkoABOpHs7PUkBmSHJB`)

**Fields:**

| Field name | Display label | Typ | Read-only? | Hinweis |
|---|---|---|---|---|
| `client` | Client | Short text | ✅ Read-only | Wird vom Workflow befüllt |
| `platform` | Platform | Short text | ✅ Read-only | Wird vom Workflow befüllt |
| `content_type` | Content Type | Short text | ✅ Read-only | Wird vom Workflow befüllt |
| `ai_angles` | Proposed Angles | Long text / Markdown | ✅ Read-only | Sofia's 3 Winkel — Reviewer liest nur |
| `sofia_decision` | Decision | Dropdown | ❌ Reviewer wählt | Optionen: `Approve: Angle 1`, `Approve: Angle 2`, `Approve: Angle 3`, `Revise` |
| `sofia_notes` | Revision Notes | Long text | ❌ Reviewer schreibt | Nur ausfüllen wenn Revise gewählt |

### Template 2: Marcus Review (`W2o71eTDvvStzR7UBni6`)

**Fields:**

| Field name | Display label | Typ | Read-only? | Hinweis |
|---|---|---|---|---|
| `angle` | Approved Angle | Short text | ✅ Read-only | Der von Sofia genehmigte Winkel |
| `post_copy` | Post Copy | Long text / Markdown | ✅ Read-only | Marcus' Post-Text |
| `image_direction` | Image Direction | Long text / Markdown | ✅ Read-only | Marcus' Bildbeschreibung |
| `taylor_preview` | Taylor Preview (AI) | Long text / Markdown | ✅ Read-only | KI-Vorschau was Taylor sehen wird |
| `marcus_decision` | Decision | Dropdown | ❌ Reviewer wählt | Optionen: `Send to Taylor`, `Edit & Regenerate` |
| `marcus_notes` | Edit Notes | Long text | ❌ Reviewer schreibt | Nur ausfüllen wenn Edit & Regenerate |

### Template 3: Taylor Review (`tjekU1jyCHgH0cbaU5UO`)

**Fields:**

| Field name | Display label | Typ | Read-only? | Hinweis |
|---|---|---|---|---|
| `post_copy` | Post Copy | Long text / Markdown | ✅ Read-only | Finaler Post-Text |
| `image_direction` | Image Direction | Long text / Markdown | ✅ Read-only | Bildbeschreibung |
| `original_brief` | Original Brief | Long text | ✅ Read-only | Topic Hint aus dem Intake-Formular |
| `ai_summary` | AI Summary | Long text / Markdown | ✅ Read-only | Taylor's KI-Zusammenfassung |
| `ai_flags` | Quality Flags | Long text / Markdown | ✅ Read-only | Liste der KI-Qualitätshinweise |
| `ai_recommendation` | AI Recommendation | Short text | ✅ Read-only | approve / needs_revision / reject_to_sofia |
| `taylor_decision` | Decision | Dropdown | ❌ Reviewer wählt | Optionen: `Approve`, `Back to Marcus`, `Back to Sofia` |
| `taylor_notes` | Feedback Notes | Long text | ❌ Reviewer schreibt | Feedback für die Revision |

---

## Step 4: Get Template IDs

After creating each template in gotoHuman:
1. Open the template
2. Copy the Template ID from the URL or settings panel
3. Use these IDs in the n8n gotoHuman nodes

---

## Step 5: Webhook Configuration

In n8n, each gotoHuman node gets a webhook URL automatically.
Set gotoHuman webhook mode to **adhoc** in each template — n8n provides dynamic URLs per workflow execution.

---

## Slack Notifications

gotoHuman can send Slack DMs or channel messages when a review is ready.
Configure in gotoHuman → Integrations → Slack.

---

## Testing

1. Trigger the workflow with TB-01 data
2. Check gotoHuman Agent Inbox for Sofia's review request
3. Approve Angle 1
4. Verify Marcus review appears with post copy + Taylor preview
5. Click "Send to Taylor"
6. Verify Taylor review appears
7. Click "Approve"
8. Check Google Sheets for the logged row
