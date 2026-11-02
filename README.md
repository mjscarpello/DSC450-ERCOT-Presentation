# ERCOT demand forecasting | DSC 450 Project 2

**Forecasting Next-Day Hourly Electricity Demand in ERCOT**

Hali Sarah Parsons, Andrea Barfield and Matthew Scarpello

This project examines hourly electricity demand, compares statistical and machine-learning forecasts, and evaluates a hybrid forecast across the full test year and the highest-demand hours. The report and presentation discuss both the results and the limits of applying retrospective experiments to operational decisions.

[Open the project website and watch the presentation](https://mjscarpello.github.io/DSC450-ERCOT-Presentation/)

## Final deliverables

| Deliverable | Location |
|---|---|
| Report / white paper | [Final Milestone 2 report (PDF)](research/reports/Milestone_2_ERCOT_Demand_Prediction_FINAL.pdf) |
| Recorded presentation | [Watch on the website](https://mjscarpello.github.io/DSC450-ERCOT-Presentation/#presentation) · [Final presentation release](https://github.com/mjscarpello/DSC450-ERCOT-Presentation/releases/tag/project2-milestone3-final) · [Download MP4](https://github.com/mjscarpello/DSC450-ERCOT-Presentation/releases/download/project2-milestone3-final/ERCOT.electricity.demand.forcasting.project.2.mp4) · 18 minutes 39 seconds |
| Q&A | [Ten stakeholder questions and answers](research/qa/stakeholder_questions.md) |
| Final visualization notebook | [Complete final notebook with saved outputs](research/notebooks/originals/DSC450_ERCOT_Full_Visualization_Hybrid_model.ipynb) |
| Code and reproduction | [Notebook guide](research/docs/NOTEBOOK_GUIDE.md) · [Data guide](research/data/README.md) · [Validation results](research/validation/REPOSITORY_CHECKS.json) |

The final report, complete 104-cell visualization notebook and recorded presentation are preserved as supplied. Earlier report and notebook versions are retained for research provenance and clearly identified in their folder guides.

## Research notebooks

The [final visualization notebook](research/notebooks/originals/DSC450_ERCOT_Full_Visualization_Hybrid_model.ipynb) is the primary visualization source. The numbered notebooks provide separate reproduction and reference workflows:

| Notebook | Purpose |
|---|---|
| [01_data_wrangling.ipynb](research/notebooks/01_data_wrangling.ipynb) | EIA-930 cleaning and feature construction. The original raw snapshot is unavailable, so this workflow has not been rerun. |
| [02_model_training.ipynb](research/notebooks/02_model_training.ipynb) | Statistical and boosting-model training. Syntax checked; model training has not been rerun. |
| [03_visualization.ipynb](research/notebooks/03_visualization.ipynb) | Historical exploration and forecast comparison, including the opposite-direction error scatterplot. |
| [04_presentation_research.ipynb](research/notebooks/04_presentation_research.ipynb) | Reconciliation of presentation statistics and supporting research figures. |

### Reproduce the evaluated results

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r research/requirements.txt
python research/tools/run_notebooks.py
python research/tools/verify_submission.py
```

The run command executes notebooks 03 and 04 using the supplied data. Generated figures go to `research/figures`, temporary analysis outputs to `research/outputs`, and validation evidence to `research/validation`. Original notebooks and presentation media remain unchanged. See the [notebook guide](research/docs/NOTEBOOK_GUIDE.md) for execution details and the [scientific limitations](research/docs/LIMITATIONS.md) for interpretation boundaries.

The [source inventory](research/SOURCE_INVENTORY.json) records original filenames, file hashes and the published video location.

## Reference website

The [ERCOT project website](https://mjscarpello.github.io/DSC450-ERCOT-Presentation/) provides an additional way to explore the research questions, figures and conclusions.
