# Supplied research data

- **eia930_erco_cleaned.csv**: Sarah's cleaned EIA-930 demand/features snapshot, 41,616 consecutive hourly rows, January 2022 through September 2026 (UTC). No raw-data rebuild is claimed.
- **ercot_model_predicitons_comparison_with_hybrid.csv**: Andrea's supplied 8,760-hour forecast export, October 2025 through September 2026. The misspelling `predicitons` is retained deliberately. Includes observed demand, the operator benchmark, six original team series and the fixed 50/50 hybrid.
- **eia930_erco_weather.csv**: the supplied merged historical observed-weather dataset used by the modeling source. It is not an advance weather forecast. Its presence supports source inspection; it does not certify operational feature availability or a full weather-model retraining.

The shared leaderboard uses 8,640 rows after dropping unavailable comparison forecasts. In particular, the ERCOT forecast is missing on 120 holdout hours; no missing operator forecast is imputed. The highest-demand cutoff uses all 8,760 observed holdout values and yields 88 peak hours in the common sample.

Input files are preserved byte-for-byte. SHA-256 values and original names are in ../SOURCE_INVENTORY.json. Original sources are EIA Form 930 and Open-Meteo as cited by the team report. These are supplied research snapshots; no independent raw-EIA authenticity or live issuance-time audit is claimed.

The original **eia930_erco_hourly.csv** raw extract is not available. It is intentionally not fabricated from the cleaned data.
