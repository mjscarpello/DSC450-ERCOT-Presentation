# Ten stakeholder questions and answers

Written Q&A corresponding to the ten questions and answers in the [user-designated final report](../reports/Milestone_2_ERCOT_Demand_Prediction_FINAL.pdf). Answers are unchanged from the earlier extraction and checked against the final PDF. This is written Q&A, not evidence of a recorded/live Q&A.

## 1. What business decision does the project inform?

Day-ahead load projections can inform generation scheduling, reserve planning, and electricity purchases. This study evaluates forecast accuracy rather than estimating financial losses, dispatch feasibility, or the operational consequences of a particular prediction error.

## 2. What exactly are we predicting?

The prediction target is realized electricity consumption in ERCOT during each hourly interval, recorded as demand_mwh in MWh. The forecasting objective is to estimate those values in advance using historical and calendar information, with supplementary weather features examined in selected models.

## 3. Why use ERCOT’s published forecast?

ERCOT's reported day-ahead forecast supplies an independently produced reference using the same underlying demand outcome. It places the team's results in an operational context, although a valid performance comparison also requires consistent prediction horizons and information availability.

## 4. Does adding weather always help?

No. Weather-enhanced XGBoost improved relative to the model without weather, whereas the tested rolling SARIMAX specification performed slightly worse than rolling SARIMA. The result demonstrates model-specific value, not a causal guarantee that adding weather will improve forecasting accuracy.

## 5. Which team model performed best?

The 50/50 hybrid of rolling SARIMA and weather-enhanced XGBoost performed the best overall among the team models, reducing MAE by approximately 52% relative to the seasonal naïve baseline. However, it was not the strongest during peak demand, where rolling SARIMA and weather SARIMAX were far more accurate.

## 6. Why didn’t any model beat ERCOT?

ERCOT forecasts with weather predictions, detailed regional load data, and operational information unavailable in public historical records. Our models used only past demand, calendar patterns, and observed temperatures.

## 7. How do the models perform on the highest-demand hours?

In the top 1% of demand hours, rolling SARIMA (1,242 MWh MAE) and weather SARIMAX (1,176 MWh) came close to ERCOT (1,158 MWh). The 50/50 hybrid had an MAE of approximately 3,189 MWh, performing better than XGBoost models which under-forecast every peak hour by over 6,000 MWh on average, likely because tree models cannot predict beyond the demand levels seen in training.

## 8. Is the comparison with ERCOT fair?

Partly. All models were scored on the same 8,640 hours, but they did not forecast under identical conditions. ERCOT issues forecasts in advance with weather predictions and operational information, while some of our models used observed historical temperatures, which gives them an advantage ERCOT does not have. Therefore, the comparison does not establish equivalent predictor availability or forecast-issuance conditions.

## 9. Could this model be used operationally today?

No. It is a retrospective study. Operational use would require fixed forecast-issuance times, weather forecasts instead of observations, regular retraining, and better peak-hour performance.

## 10. What would most improve the forecasts?

The current 50/50 hybrid improves average forecast error, but its weaker peak-hour accuracy shows why a single fixed blend may not suit every demand condition. Future work should use advance-available weather forecasts, account for demand growth, and test model weights that adapt to conditions known at forecast issuance, without relying on actual demand to choose the model.
