# Future presentation handoff — not an approved script

This context web is intended to be the **research memory** used before narration or Studio S orchestration begins.

A future scene object could link to a scientific claim, one or more figures, supporting numerical facts, caveats and a speaker. For example:

```json
{
  "scene_id": "S08",
  "approved": false,
  "speaker": null,
  "topic": "Average accuracy can conceal peak-demand weakness",
  "research_claims": ["FIND-OVERALL", "FIND-PEAK"],
  "numeric_evidence": [
    "METRIC-OVERALL-HYBRID_50_50",
    "METRIC-TOP_1PCT-ROLLING_SARIMA",
    "METRIC-TOP_1PCT-HYBRID_50_50"
  ],
  "figures": ["FIG-F14", "FIG-F17"],
  "scientific_caveats": ["LIMIT-PEAK-BIN", "LIMIT-ORIGIN"],
  "narration": null,
  "audio_clip": null,
  "studio_s_cues": []
}
```

The above is an **illustration of how to reference the web**, not a real approved presentation scene, speaking assignment or native Studio S schema. The actual importer should be designed after auditing the relevant Studio S specification.

Recommended future workflow:

1. Confirm and lock the exact research claim and evidence.
2. Use `trace` and `inspect` to recover supporting numbers and context.
3. Select an approved figure by stable ID, preserving notebook original and source data.
4. Add the exact caveat that bounds the interpretation.
5. Request a teammate's approval of the relevant explanation, then draft a narration line.
6. Only after recording: identify precise word timings for animated highlights.
7. Have Studio S consume a mapped scene manifest; do not assume a new JSON format automatically imports into the present application.

The graph is deliberately separate from scripts and audio. Research findings remain stable even if the scene order, editing style, or selected speaker changes.
