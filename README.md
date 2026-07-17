# Opinion Dynamics in AI-Agent vs. Human Online Communities — Replication Package

De-identified data and code accompanying the manuscript comparing opinion
dynamics and interaction structure in an AI-agent social network (Moltbook)
and a human platform (Reddit).

> **Anonymized for double-blind review.** Author and affiliation information is
> intentionally omitted. This mirror is a review-time placeholder; the canonical
> repository and citation will be provided upon publication.

## What is included

This package contains **de-identified derived data only** — no post text and no
user identities. Content is represented by classifier-assigned stance labels;
users are replaced by opaque sequential IDs (`a1`, `a2`, …) with no recoverable
relation to real accounts; timestamps are coarsened to calendar date.

```
data/
  posts_deident.csv    one row per post: opaque IDs, platform, community, date,
                       removal flag, and stance under three classifiers
                       (gpt-4o-mini, Gemini 2.5 Flash, Claude Haiku 4.5)
  reply_edges.csv      reply network as opaque author-to-author edges
  gold_standard.csv    192 human-annotated validation posts: four anonymized
                       annotators' labels, majority label, and classifier labels
  structural_aggregates.csv
                       platform x community aggregates (incl. pooled and
                       technology-excluded rows) behind the structural ratios
  DATA_DICTIONARY.md   column-level documentation
reproduce.py           regenerates the paper's key results from the CSVs above
pipeline/              methodology scripts (classification + annotation tool);
                       provided for transparency — they require the raw corpus
                       and API access and are NOT runnable from this package
```

## Reproducing the results

```bash
pip install -r requirements.txt
python3 reproduce.py
```

This regenerates, directly from the released de-identified data:

- content-removal rates per platform/community,
- RQ1 opinion-entropy convergence (cross-platform effect size) under each of the
  three stance classifiers,
- RQ2 echo-chamber E-I index and the "AI-weaker" community count, including the
  sensitivity check that restricts to stance-bearing (non-neutral) authors.

The released data reproduce the manuscript's reported values (e.g., the RQ1
cross-platform effect size and the per-community removal rates) exactly.

## Data and ethics

- Only publicly available data were analyzed. No post content or account
  identifiers are redistributed here.
- Author IDs are opaque sequential labels assigned at export time; they cannot be
  mapped back to original accounts from this package.
- Stance labels are model outputs, not ground truth; see the manuscript's
  measurement-validity analysis and `gold_standard.csv` for the human comparison.

**Linkage-risk note.** Each post row retains its calendar date (required to
reproduce the daily opinion-entropy trends). No post text, title, word count,
URL, timestamp-of-day, or account identifier is included, so rows cannot be
linked to originals from this package alone. We judge the residual
re-identification risk to be low.

## License

Code and derived data are released under the MIT License (see `LICENSE`).
