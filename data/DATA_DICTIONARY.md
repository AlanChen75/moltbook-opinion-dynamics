# Data Dictionary

All identifiers are opaque sequential labels assigned at export; they cannot be
mapped back to original posts or accounts. No post text is included.

## posts_deident.csv

One row per post (77,442 rows).

| column | type | description |
|--------|------|-------------|
| opaque_post_id | str | `p1`, `p2`, … — opaque post identifier |
| opaque_author_id | str | `a1`, `a2`, … — opaque author identifier (consistent with reply_edges.csv) |
| platform | str | `moltbook` (AI agents) or `reddit` (human) |
| community | str | one of: ai, consciousness, crypto, philosophy, security, technology |
| date | str | posting date, `YYYY-MM-DD` (time-of-day removed) |
| is_removed | 0/1 | 1 if the post was removed/deleted or empty (coded NEUTRAL downstream) |
| stance_gpt4omini | str | stance under gpt-4o-mini (SUPPORTIVE/NEUTRAL/OPPOSING); the manuscript's primary classifier |
| stance_gemini | str | stance under Gemini 2.5 Flash (S/N/O); empty if the post was not classified (short/removed) |
| stance_claude | str | stance under Claude Haiku 4.5 (S/N/O); empty if not classified |

Note: `stance_gpt4omini` labels every post (removed/short coded NEUTRAL by the
original pipeline); `stance_gemini`/`stance_claude` are empty for unclassified
(short/removed) posts, which downstream analyses treat as NEUTRAL.

## reply_edges.csv

One row per reply edge (706,819 rows); self-replies excluded.

| column | type | description |
|--------|------|-------------|
| opaque_replier_id | str | author who replied (`a…`) |
| opaque_author_id | str | author of the post being replied to (`a…`) |
| community | str | community of the interaction |
| platform | str | platform of the interaction |

## gold_standard.csv

192 human-annotated validation posts.

| column | type | description |
|--------|------|-------------|
| opaque_sample_id | str | `s1`…`s192` |
| community | str | community |
| platform | str | platform |
| ann1 … ann4 | str | four anonymized annotators' labels (S/N/O/NA); NA = stance axis not applicable |
| human_majority | str | majority label among retained annotators; `TIE` where no majority |
| stance_gpt4omini | str | gpt-4o-mini label |
| stance_gemini | str | Gemini label (OpenRouter endpoint) |
| stance_claude | str | Claude label (OpenRouter endpoint) |
