#!/usr/bin/env python3
"""
Reproduce the key opinion-dynamics results from the de-identified release data.

Runs entirely on data/posts_deident.csv + data/reply_edges.csv (no raw text, no
identities, no API needed). Regenerates:
  - content-removal rates per platform/community
  - RQ1: daily opinion-entropy convergence slopes + cross-platform effect size,
         under each stance classifier
  - RQ2: echo-chamber E-I index per community, and the "AI-weaker" count
  - RQ2 sensitivity: E-I restricted to stance-bearing (non-neutral) authors

Three classifiers are provided as separate columns (gpt-4o-mini, Gemini, Claude)
so readers can see how conclusions depend on the stance-measurement choice.

Usage:  python3 reproduce.py
Requires: numpy, scipy  (see requirements.txt)
"""

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import linregress, mannwhitneyu

DATA = Path(__file__).parent / "data"
COMMUNITIES = ["ai", "consciousness", "crypto", "philosophy", "security", "technology"]
CLASSIFIERS = ["stance_gpt4omini", "stance_gemini", "stance_claude"]
NORM = {"S": "SUPPORTIVE", "N": "NEUTRAL", "O": "OPPOSING",
        "SUPPORTIVE": "SUPPORTIVE", "NEUTRAL": "NEUTRAL", "OPPOSING": "OPPOSING"}


def eff(raw):
    """Canonical stance; empty (short/removed, unclassified) -> NEUTRAL."""
    return NORM.get((raw or "").strip().upper(), "NEUTRAL")


def load():
    posts = list(csv.DictReader(open(DATA / "posts_deident.csv")))
    edges = list(csv.DictReader(open(DATA / "reply_edges.csv")))
    return posts, edges


def removal_rates(posts):
    print("=" * 64)
    print("Content removal rate per platform/community")
    print("=" * 64)
    for plat in ["reddit", "moltbook"]:
        print(f"  {plat}:")
        for comm in COMMUNITIES:
            rows = [p for p in posts if p["platform"] == plat and p["community"] == comm]
            rem = sum(1 for p in rows if p["is_removed"] == "1")
            print(f"    {comm:<14} {rem/len(rows)*100:5.1f}%  ({rem}/{len(rows)})")


def entropy(stances, k=3):
    c = Counter(stances)
    t = sum(c.values())
    if not t:
        return 0.0
    probs = [c.get(s, 0) / t for s in ["SUPPORTIVE", "NEUTRAL", "OPPOSING"]]
    return -sum(p * math.log2(p) for p in probs if p > 0) / math.log2(k)


def rq1(posts, col):
    slopes = {"moltbook": [], "reddit": []}
    for comm in COMMUNITIES:
        for plat in ["moltbook", "reddit"]:
            daily = defaultdict(list)
            for p in posts:
                if p["community"] == comm and p["platform"] == plat and p["date"]:
                    daily[p["date"]].append(eff(p[col]))
            series = [entropy(daily[d]) for d in sorted(daily) if len(daily[d]) >= 5]
            if len(series) >= 7:
                s, *_ = linregress(np.arange(len(series)), series)
                slopes[plat].append(s)
    m, r = slopes["moltbook"], slopes["reddit"]
    u, p = mannwhitneyu(m, r, alternative="two-sided")
    d = (np.mean(m) - np.mean(r)) / (np.std(m + r) + 1e-10)
    return round(float(d), 3), round(float(p), 3)


def author_dom(posts, col, comm, plat, drop_neutral=False):
    cnt = defaultdict(Counter)
    for p in posts:
        if p["community"] == comm and p["platform"] == plat and p["opaque_author_id"]:
            cnt[p["opaque_author_id"]][eff(p[col])] += 1
    dom = {a: c.most_common(1)[0][0] for a, c in cnt.items()}
    return {a: s for a, s in dom.items() if not (drop_neutral and s == "NEUTRAL")}


def ei(edges, dom, comm, plat):
    internal = external = 0
    for e in edges:
        if e["community"] == comm and e["platform"] == plat:
            s1, s2 = dom.get(e["opaque_replier_id"]), dom.get(e["opaque_author_id"])
            if s1 and s2:
                internal += (s1 == s2)
                external += (s1 != s2)
    t = internal + external
    return (external - internal) / t if t else 0.0


def rq2(posts, edges, col, drop_neutral=False):
    weaker = 0
    for comm in COMMUNITIES:
        m = ei(edges, author_dom(posts, col, comm, "moltbook", drop_neutral), comm, "moltbook")
        r = ei(edges, author_dom(posts, col, comm, "reddit", drop_neutral), comm, "reddit")
        weaker += m > r
    return weaker


def structural():
    """RQ3 structural robustness from data/structural_aggregates.csv + posts_deident.
    Thread size and latency come from the released platform/community aggregates
    (per-comment data are not released); the Gini of per-author post counts is
    recomputed directly from posts_deident.csv."""
    agg = {(r["platform"], r["community"]): r
           for r in csv.DictReader(open(DATA / "structural_aggregates.csv"))}
    print("=" * 64)
    print("RQ3 structural comparison (pooled vs excluding technology pair)")
    print("=" * 64)
    for label in ["ALL", "ALL_EXCL_TECHNOLOGY"]:
        m, r = agg[("moltbook", label)], agg[("reddit", label)]
        md, rd = float(m["mean_comments_per_post"]), float(r["mean_comments_per_post"])
        ml, rl = float(m["median_first_reply_latency_s"]), float(r["median_first_reply_latency_s"])
        print(f"  {label}:")
        print(f"    comments/post   M {md:5.2f}  R {rd:6.2f}   ratio {rd/md:.1f}x")
        print(f"    median latency  M {ml:6.1f}s R {rl:6.1f}s  ratio {rl/ml:.1f}x")
    posts = list(csv.DictReader(open(DATA / "posts_deident.csv")))
    for label, drop_tech in [("ALL", False), ("ALL_EXCL_TECHNOLOGY", True)]:
        ginis = {}
        for plat in ["moltbook", "reddit"]:
            counts = Counter(p["opaque_author_id"] for p in posts
                             if p["platform"] == plat
                             and not (drop_tech and p["community"] == "technology"))
            sc = np.sort(np.array(list(counts.values()), dtype=float))
            n = len(sc)
            ginis[plat] = (2 * np.sum(np.arange(1, n + 1) * sc) - (n + 1) * np.sum(sc)) / (n * np.sum(sc))
        print(f"  {label}: Gini  M {ginis['moltbook']:.3f}  R {ginis['reddit']:.3f}")


def main():
    posts, edges = load()
    print(f"loaded {len(posts)} posts, {len(edges)} reply edges\n")
    removal_rates(posts)
    print("\n" + "=" * 64)
    print("RQ1 opinion-entropy convergence (cross-platform)")
    print("=" * 64)
    for col in CLASSIFIERS:
        d, p = rq1(posts, col)
        print(f"  {col:<18} Cohen's d = {d:+.3f}   Mann-Whitney p = {p:.3f}")
    print("  (sign flips across classifiers; all non-significant -> inconclusive)")
    print("\n" + "=" * 64)
    print("RQ2 echo chamber: 'AI weaker' count (all authors vs stance-bearing only)")
    print("=" * 64)
    for col in CLASSIFIERS:
        wa = rq2(posts, edges, col, False)
        wb = rq2(posts, edges, col, True)
        print(f"  {col:<18} all-authors {wa}/6   stance-bearing-only {wb}/6")
    print("  (majority 'AI weaker' collapses once neutral-dominant authors are dropped)")
    print()
    structural()


if __name__ == "__main__":
    main()
