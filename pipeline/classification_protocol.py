#!/usr/bin/env python3
"""
Stance-classification protocol (methodology reference).

Documents the EXACT zero-shot prompting used to label posts under each language
model. It is a reference, not a runnable pipeline: classification requires the
raw post text (not redistributed) and a language-model API key. The resulting
labels are provided per post in ../data/posts_deident.csv, and the human
comparison set is in ../data/gold_standard.csv.

Key protocol choices (identical across all three classifiers, for comparability):
  - zero-shot, temperature 0
  - reasoning/thinking disabled (deterministic, and avoids garbling the
    numbered-list output format)
  - the same system prompt and per-community stance axis for every model
  - posts batched; each post truncated to 300 characters for the prompt
"""

import re

# Per-community stance axis (defines what SUPPORTIVE vs OPPOSING means).
COMMUNITY_AXES = {
    "crypto": "Bullish/pro-crypto/pro-adoption = S | Bearish/scam/anti-crypto/bubble = O",
    "philosophy": "Agrees with/extends the argument = S | Counterargument/challenges premises = O",
    "ai": "AI-optimist/beneficial/pro-development = S | AI-pessimist/warns risks/calls for restriction = O",
    "technology": "Pro-innovation/enthusiastic about tech = S | Tech-critical/warns of downsides = O",
    "consciousness": "Affirms AI/machine consciousness = S | Denies AI consciousness = O",
    "security": "Treats threat as real/serious = S | Dismisses threat as overblown/FUD = O",
}

SYSTEM_PROMPT = """You are a stance classifier for social media posts. For each numbered post, output ONLY its number and label separated by colon. One per line. No explanations.

Labels:
- S (SUPPORTIVE): author clearly advocates, agrees, is enthusiastic about the stance axis topic
- O (OPPOSING): author clearly criticizes, disagrees, warns against the stance axis topic
- N (NEUTRAL): informational, questioning, balanced, ambiguous, reflective, off-topic, meta-discussion, or too short to judge

Rules:
- Label the AUTHOR's stance, not the topic's valence (a post about a crypto crash can be S if author sees buying opportunity)
- Default to N when uncertain — do not over-classify
- Sarcasm: label by intended meaning
- Pure questions without direction: N
- Philosophical musings without clear position: N"""


def build_prompt(community, posts):
    """Format a batch of (up to 300-char) posts into the numbered prompt."""
    axis = COMMUNITY_AXES.get(community, "Agrees = S | Disagrees = O")
    lines = [f"Community: {community}\nStance axis: {axis}\n"]
    for i, text in enumerate(posts, 1):
        t = text.strip()
        if len(t) > 300:
            t = t[:300] + "..."
        lines.append(f"{i}. {t}")
    lines.append(f"\nOutput {len(posts)} lines, format: number:label")
    return "\n".join(lines)


def parse_labels(text, n_expected):
    """Parse 'number:label' lines; return {index: S/N/O} or None on count mismatch."""
    labels = {}
    for m in re.finditer(r"^\s*(\d+)\s*[:.\)]\s*([SNO])\b", text or "", re.M | re.I):
        labels[int(m.group(1))] = m.group(2).upper()
    return labels if len(labels) == n_expected else None


# API request body used for every model (temperature 0, reasoning disabled):
#   {
#     "model": <model id>,
#     "temperature": 0,
#     "reasoning": {"enabled": False},
#     "messages": [{"role": "system", "content": SYSTEM_PROMPT},
#                  {"role": "user",   "content": build_prompt(community, batch)}],
#   }
# The API key is supplied via an environment variable; no key is stored here.
