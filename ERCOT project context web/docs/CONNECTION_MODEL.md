# How research connections work

This is a **knowledge graph**, not a model of statistical relationships.

## Anatomy of a node

Every node has `id`, `type`, `title`, `summary`, `status` and `sources`. Many also have numerical `value` and `unit`, a `research_question`, or a `asset_path` linked to an extracted PNG. The stable ID can be referenced from a future script or scene manifest.

| Status | Interpretation |
|---|---|
| `csv-verified` | Arithmetic independently recalculated on the supplied model predictions CSV, without independently validating the original training process |
| `source-supported` | Stated in the team's supplied report or notebook; not necessarily independently reproduced |
| `conversation-supported` | Team decision or intent previously discussed |
| `interpretive` | Hypothesis, interpretive explanation or an inferred question; not a demonstrated causal effect |
| `user-plan` | Planned activity, not completed |
| `open` | Unverified or unresolved requirement |

## Anatomy of a link

```json
{
  "from": "METRIC-OVERALL-HYBRID_50_50",
  "to": "FIND-OVERALL",
  "relation": "contributes matched-error result",
  "weight": 5,
  "kind": "evidence",
  "flow": "dependency",
  "rationale": "MAE calculated on the same common forecast-available hours."
}
```

The `weight` is an **editorial closeness-of-relationship scale**:

| Weight | Meaning | Example |
|---|---|---|
| 5 | Direct numerical/computational derivation | Prediction CSV → verified model MAE |
| 4 | Direct documented scientific relationship | Notebook → F17 chart; report → method |
| 3 | Meaningful but interpretive relationship | Forecast error complementarity → exploratory hybrid idea |
| 2 | Contextual/background or co-occurring relationship | One document describes a finding |
| 1 | Tentative interpretation/future proposal | Tree extrapolation as a possible cause |

**Never interpret the weight as numerical confidence or as a measured model parameter.** If a model predictor correlates with temperature, that correlation must be independently calculated; the graph's weight doesn't measure it.

Other edge fields:

- `kind`: `provenance`, `evidence`, `dataflow`, `quantitative`, `reasoning`, `caveat`, `organization`, `presentation`, and preserved original links.
- `flow`: `dependency` when the target uses/depends upon the origin as documented; `association` for contextual links.
- `rationale`: short explanation for why the link exists.
- Links are **directed and can have multiple types between the same two nodes**. A shortest path can traverse associations in either direction for discovery only, and does not assert reverse causality. Downstream-impact queries follow only `dependency` edges in the stored direction.

## Graph traversal

- `inspect ID`: all source properties and neighboring relations for one node.
- `near ID --depth 2 --min-weight 4`: immediate evidence-rich connected web.
- `trace A B`: weighted shortest *explanation path*, not necessarily a causal path.
- `impact ID`: directed dependency downstream; use as a review checklist after changing data, a figure, or a claim.
- `audit`: graph integrity, valid weight values, figures with missing file paths, isolated nodes, and unknown evidence statuses.

## Updating or extending the graph

The reproducible builder is `src/ercot_web/build.py`, supplied with static configuration and source-derived `data/figure_notes.json`, `data/model_metrics.json`. Add deliberate scientific concepts to its configuration or its reviewed foundation rather than modifying only the generated HTML. Rebuild JSON, run tests, review changed data, and regenerate HTML. For a new presentation scene, connect its stable ID to the exact `FIG-*` figures, `FIND-*` claims, relevant `LIMIT-*` caveats, and speaker-owned sections.
