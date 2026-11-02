# Scientific and reproduction boundaries

1. These are retrospective experimental results. Matching target timestamps does not establish equal forecast issue times, horizons, update schedules or information availability.
2. Historical observed weather is not a forecast available in advance. Weather features require an issuance-time audit before operational claims.
3. High-demand groups are selected after observing actual load. They diagnose past performance, rather than identify tomorrow's peak hours in advance.
4. The hybrid is a fixed 50/50 arithmetic average. No tested demand-regime switching policy, dispatch-cost model, reserve calculation or outage-risk model is provided.
5. Opposite signs occur in 4,022 of 8,640 matched hours. Pearson r is about +0.213. Some errors offset; the two error series are not negatively correlated overall. Improvement must be evaluated on the hybrid's actual absolute errors.
6. The raw EIA hourly snapshot is unavailable, so the cleaning workflow is preserved but not rerun. Frozen cleaned data and predictions support the verified visualization/evaluation reproduction.
7. Original rolling model training was not rerun here. Code syntax validation is not model retraining or leakage verification. The merged observed-weather source is now included, but the old temperature figures have not been reverse-engineered or silently certified as source-reproduced.
8. The failed year-long static SARIMA prediction trace is unavailable. The final rolling forecast cannot reconstruct that failed experiment; it is not fabricated.
9. The report versions are preserved unchanged. Earlier versions predate hybrid results; consult reports/README.md. Hypotheses about why models differ should not be treated as causal proof.
10. Matthew's final exported video and latest local Studio S edits were not received in this pass. No older preview is claimed to be the finished presentation.
