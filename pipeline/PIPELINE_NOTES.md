# Pipeline (methodology transparency)

These files document how the stance labels and the human-annotation validation
set were produced. They are references, **not runnable from this package** — the
raw post text and language-model API access are not redistributed here. The
runnable, self-contained reproduction of the paper's results is `../reproduce.py`,
which operates on the released de-identified data.

| file | role |
|------|------|
| `classification_protocol.py` | the exact zero-shot prompting protocol: system prompt, per-community stance axis, prompt formatting, temperature 0, reasoning disabled. API keys are supplied via environment variables — none are stored here |
| `annotation_guideline.md` | the stance-annotation codebook given to annotators (label definitions, per-community stance axes, calibration rules, the four labels including "axis not applicable") |

The stance labels these produce are provided per post in
`../data/posts_deident.csv`; the human labels are in `../data/gold_standard.csv`.
