# Workflow Architecture

## Overview

Three-stage Human-in-the-Loop (HITL) content pipeline. Each stage has an AI agent + gotoHuman review. Rejections loop back with explicit feedback. All decisions are logged to Google Sheets.

```
Form (Intake)
    ↓
Set (Load context: Brand Guide, Platform Specs)
    ↓
Sofia AI (generate 3 angles)
    ↓
Sofia gotoHuman Review
    ├── Approve → Marcus
    └── Revise → Sofia AI (with feedback)
    ↓
Marcus AI (write post + visual direction)
    ↓
Claude API Preview (Taylor's perspective — JSON only)
    ↓
Marcus gotoHuman Review
    ├── Send to Taylor → Taylor AI
    └── Edit & Regenerate → Marcus AI (with feedback + new preview)
    ↓
Taylor AI (QC summary + flags)
    ↓
Taylor gotoHuman Review
    ├── Approve → Google Sheets (FINAL)
    ├── Back to Marcus → Marcus AI
    └── Back to Sofia → Sofia AI
    ↓
Google Sheets (log final post)
```

---

## Stage 1: Sofia (Content Strategy)

**Purpose:** Generate 3 content angle options for the human reviewer.

**Input:**
- Client, Platform, Content Type, Topic Hint, Tone Note (from form)
- Loopin Brand Guide (system context)
- Relay Platform Playbook (system context)
- `previous_feedback` (if revision loop)

**Output:** 3 titled angles with rationale

**Review fields (gotoHuman):**
- `client`, `platform`, `content_type` — context display
- `ai_angles` — Sofia's 3 options (markdown)
- `sofia_decision` — dropdown: "Approve: [angle title]" | "Revise"
- `sofia_notes` — free text, required on Revise

**Routing:**
- Approve → Marcus AI
- Revise → Sofia AI (sofia_notes → previous_feedback)

---

## Stage 2: Marcus (Creative)

**Purpose:** Write post copy + image direction based on Sofia's approved angle.

**Key feature — Taylor Preview Loop:**
After Marcus generates, a Claude API call simulates Taylor's review and returns a JSON summary with quality flags. Marcus sees this preview in his gotoHuman form and can self-correct before Taylor sees the post.

**Input:**
- Approved angle from Sofia
- Platform, Content Type, Brand Guide, Platform Playbook
- `previous_feedback` (if revision loop)

**Output:** Post copy + specific image direction

**Claude API Preview (before Marcus review):**
- Input: post copy + image direction + original brief + brand context
- Output: JSON `{ summary, quality_flags[], recommendation, reasoning }`
- On parse failure: empty preview, don't block workflow

**Review fields (gotoHuman):**
- `angle`, `post_copy`, `image_direction` — content display
- `taylor_preview` — AI preview markdown (summary + flags + recommendation)
- `marcus_decision` — dropdown: "Send to Taylor" | "Edit & Regenerate"
- `marcus_notes` — feedback for next iteration

**Routing:**
- Send to Taylor → Taylor AI
- Edit & Regenerate → Marcus AI (marcus_notes → previous_feedback, new preview generated)

---

## Stage 3: Taylor (Final QC)

**Purpose:** Final quality check before the post is approved.

**Input:**
- Post copy + image direction (from Marcus)
- Original brief (from intake form)
- Brand Guide + Platform Playbook
- Marcus preview summary

**Output:** Summary, quality flags, AI recommendation

**Review fields (gotoHuman):**
- `post_copy`, `image_direction`, `original_brief` — context
- `ai_summary`, `ai_flags`, `ai_recommendation` — Taylor's AI analysis
- `taylor_decision` — dropdown: "Approve" | "Back to Marcus" | "Back to Sofia"
- `taylor_notes` — feedback

**Routing:**
- Approve → Google Sheets
- Back to Marcus → Marcus AI (taylor_notes → previous_feedback)
- Back to Sofia → Sofia AI (taylor_notes → previous_feedback)

---

## Google Sheets Output Schema

| Column | Value |
|---|---|
| `timestamp` | Workflow start time |
| `client` | From intake |
| `platform` | From intake |
| `content_type` | From intake |
| `approved_angle` | Sofia's chosen angle |
| `post_copy` | Marcus final |
| `image_direction` | Marcus final |
| `iterations_sofia` | Number of Sofia revisions |
| `iterations_marcus` | Number of Marcus revisions |
| `total_iterations` | Sum |
| `approval_time_seconds` | Seconds from intake to final approval |
| `status` | APPROVED \| REJECTED |
| `taylor_approval_round` | 1 = first try, 2+ = went back |

---

## Loop protection

Max 3 revisions per stage. Track `iterations_sofia` and `iterations_marcus` counters. After 3, send Slack alert and pause workflow for manual review.

---

## Context loading (client-agnostic design)

Brand context is loaded once at the start in a Set node:
```
brand_name: "Loopin"
brand_guide_full: [full markdown from resources/loopin-brand-guide.md]
platform_playbook_full: [full markdown from resources/relay-platform-playbook.md]
```

All prompts reference `{{ brand_guide_full }}` and `{{ platform_playbook_full }}`.
To swap clients: change only the Set node values — no prompt edits needed.
