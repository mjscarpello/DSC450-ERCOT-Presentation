# Scientific boundaries / source-of-truth rules

- **Forecast target**: ERCOT actual hourly electricity consumption, `demand_mwh` / `ACTUAL_DEMAND_MWH`, measured in MWh per hour interval.
- **Historical coverage**: 41,616 hourly EIA-930 demand observations (January 2022 through September 2026). See the supplied Milestone 2 report's Methods/Analysis.
- **Test evaluation**: 8,760 hours (Oct 2025–Sep 2026); 120 ERCOT benchmark forecast hours unavailable; 8,640 hours used for the eight-series matched comparison.
- **Best team approach on the shared sample**: the fixed 50/50 mean of rolling SARIMA and weather XGBoost predictions. It is not a new independently fitted predictive model.
- **Magnitude and direction differ**: mean absolute error averages magnitude; signed forecast minus observed demand distinguishes overforecast/underforecast.
- **Peak analysis is retrospective**: 88 matched hours meet the 99th percentile cutoff defined across the full test year's observed demand. These 88 outcomes cannot be identified prospectively without a separate forecast of future regime membership.
- **Model behavior vs causes**: XGBoost underforecasted every one of the 88 highest-load matched hours, but tree extrapolation is a plausible mechanism, not a causal experiment isolating it.
- **Weather caveat**: some enhanced models use observed temperatures or historical temperature summaries; those are not equivalent to advance weather forecasts.
- **Timing caveat**: SARIMA/SARIMAX's rolling 24-hour updates, target-relative XGBoost lag features and Prophet's longer static forecast have not all been proven to follow identical forecast-issuance information constraints. Identical target-hour MAE is not an identical operational contest.
- **Real-world impact**: these retrospective metrics do not measure generation scheduling cost, emergency electricity purchases, prevented outages, or avoided blackouts.
- **Exploratory 36/64 weights**: the notebook's chronological weight experiment must not supersede the team's official 50/50 result. The earlier-selected weighting did not beat the fixed hybrid in the later evaluation split.
- **Unverified**: the full original model-training code, exact each-model forecast-origin/input-availability audit, and a final Studio S integration build are not validated by this graph.

All quantitative model facts in `data/model_metrics.json` come from the user-supplied prediction export. See `src/ercot_web/metrics.py` for the exact operations.

A `source-supported` finding means it is in the submitted research documents. It does **not** mean that upstream training or any causal interpretation has been independently audited.
