#!/usr/bin/env python3
"""
Injects brand guide + platform playbook content into the workflow JSON
and substitutes credential/template ID placeholders from .env.

Usage:
  cp .env.example .env && nano .env  # fill in your IDs
  python scripts/inject_context.py
  # imports dist/relay-hitl-pipeline.json into n8n
"""

import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_env():
    env = {}
    env_file = os.path.join(BASE, ".env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def load_resource(filename):
    path = os.path.join(BASE, "resources", filename)
    with open(path, encoding="utf-8") as f:
        return f.read()

def main():
    brand_guide = load_resource("loopin-brand-guide.md")
    platform_playbook = load_resource("relay-platform-playbook.md")
    env = load_env()

    wf_path = os.path.join(BASE, "workflows", "relay-hitl-pipeline.json")
    with open(wf_path, encoding="utf-8") as f:
        raw = f.read()

    # Inject content
    raw = raw.replace(
        "PASTE_FULL_CONTENT_OF_resources/loopin-brand-guide.md_HERE",
        brand_guide
    )
    raw = raw.replace(
        "PASTE_FULL_CONTENT_OF_resources/relay-platform-playbook.md_HERE",
        platform_playbook
    )

    # Substitute credential/template placeholders
    substitutions = {
        "{{ANTHROPIC_CRED_ID}}":       env.get("ANTHROPIC_CRED_ID", "REPLACE"),
        "{{GOTOHUMAN_CRED_ID}}":       env.get("GOTOHUMAN_CRED_ID", "REPLACE"),
        "{{GOOGLE_SHEETS_CRED_ID}}":   env.get("GOOGLE_SHEETS_CRED_ID", "REPLACE"),
        "{{SOFIA_TEMPLATE_ID}}":       env.get("SOFIA_TEMPLATE_ID", "REPLACE"),
        "{{MARCUS_TEMPLATE_ID}}":      env.get("MARCUS_TEMPLATE_ID", "REPLACE"),
        "{{TAYLOR_TEMPLATE_ID}}":      env.get("TAYLOR_TEMPLATE_ID", "REPLACE"),
    }
    for placeholder, value in substitutions.items():
        raw = raw.replace(placeholder, value)

    # Validate JSON
    try:
        wf = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON parse failed after injection: {e}")
        raise

    # Write to dist/
    dist_dir = os.path.join(BASE, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    out_path = os.path.join(dist_dir, "relay-hitl-pipeline.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)

    print(f"OK  Wrote {out_path}")

    missing = [k for k, v in substitutions.items() if v == "REPLACE"]
    if missing:
        print(f"WARN Missing in .env: {', '.join(missing)}")
        print("     Update .env and re-run before importing to n8n.")
    else:
        print("    All placeholders substituted.")

if __name__ == "__main__":
    main()
