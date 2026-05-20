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

### Template 1: Sofia Review

**Fields to create in gotoHuman:**

| Field name | Display label | Type |
|---|---|---|
| `client` | Client | Text |
| `platform` | Platform | Text |
| `content_type` | Content Type | Text |
| `ai_angles` | Proposed Angles | Markdown |
| `sofia_decision` | Decision | Dropdown |
| `sofia_notes` | Revision Notes | Text |

**Dropdown options for `sofia_decision`:**
- `Approve: Angle 1`
- `Approve: Angle 2`
- `Approve: Angle 3`
- `Revise`

### Template 2: Marcus Review

**Fields to create in gotoHuman:**

| Field name | Display label | Type |
|---|---|---|
| `angle` | Approved Angle | Text |
| `post_copy` | Post Copy | Markdown |
| `image_direction` | Image Direction | Markdown |
| `taylor_preview` | Taylor's Preview | Markdown |
| `marcus_decision` | Decision | Dropdown |
| `marcus_notes` | Edit Notes | Text |

**Dropdown options for `marcus_decision`:**
- `Send to Taylor`
- `Edit & Regenerate`

### Template 3: Taylor Review

**Fields to create in gotoHuman:**

| Field name | Display label | Type |
|---|---|---|
| `post_copy` | Post Copy | Markdown |
| `image_direction` | Image Direction | Markdown |
| `original_brief` | Original Brief | Text |
| `ai_summary` | AI Summary | Markdown |
| `ai_flags` | Quality Flags | Markdown |
| `ai_recommendation` | AI Recommendation | Text |
| `taylor_decision` | Decision | Dropdown |
| `taylor_notes` | Feedback Notes | Text |

**Dropdown options for `taylor_decision`:**
- `Approve`
- `Back to Marcus`
- `Back to Sofia`

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
