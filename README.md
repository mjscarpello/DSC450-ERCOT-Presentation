# ERCOT demand forecasting | DSC 450 Project 2

Research and submission materials for **Forecasting Next-Day Hourly Electricity Demand in ERCOT**, by Hali Sarah Parsons, Andrea Barfield and Matthew Scarpello.

## Submission materials

| Required deliverable | Location | Status |
|---|---|---|
| Report / white paper | [Final Milestone 2 report (PDF)](research/reports/Milestone_2_ERCOT_Demand_Prediction_FINAL.pdf) | Exact final report designated by Matthew. Earlier versions are reference only; see [version notes](research/reports/README.md). |
| Presentation | [Final video handoff](research/presentation/README.md) | Final MP4 received and media decode checked (18:39, 40 MB). GitHub Release draft prepared; asset upload and public video link pending. |
| Q&A | [Ten stakeholder questions and answers](research/qa/stakeholder_questions.md) | Written Q&A corresponding to the final report’s ten stakeholder questions. |
| Code / link to code | [Research notebook guide](research/docs/NOTEBOOK_GUIDE.md) | Cleaning, model-training, complete visualization and presentation-research notebooks, with source data and reproducibility checks. |

The video and the final Studio S project are maintained separately from the research code. Earlier storyboard/audio drafts are **not** labeled as the final presentation. This organization does not change Matthew's completed local video or visual edits.

## Start with the research

**Authoritative final visualization notebook:** [DSC450_ERCOT_Full_Visualization_Hybrid_model.ipynb](research/notebooks/originals/DSC450_ERCOT_Full_Visualization_Hybrid_model.ipynb). Matthew supplied this complete final version: all 104 cells, including 45 code cells, and saved outputs are preserved without condensing or rerunning it. The numbered notebooks below are reproducibility/reference copies; they do not replace his final notebook.

1. [03_visualization.ipynb](research/notebooks/03_visualization.ipynb): full historical exploration and eight-series forecast comparison, including the added opposite-direction error scatterplot.
2. [04_presentation_research.ipynb](research/notebooks/04_presentation_research.ipynb): independently checked presentation numbers and research figures.
3. [01_data_wrangling.ipynb](research/notebooks/01_data_wrangling.ipynb) and [02_model_training.ipynb](research/notebooks/02_model_training.ipynb): original team workflows adapted to repository paths, with execution limits stated up front.

Unmodified original notebooks are preserved in [research/notebooks/originals](research/notebooks/originals). [Source inventory](research/SOURCE_INVENTORY.json) records their hashes and original filenames. The [data guide](research/data/README.md) explains the supplied CSVs and the historical `predicitons` filename typo.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r research/requirements.txt
python research/tools/run_notebooks.py
python research/tools/verify_submission.py
```

The run command executes notebooks 03 and 04. It does **not** retrain models, download raw data, or modify presentation media. Reproduction outputs go to `research/figures` and `research/outputs`; validation evidence goes to [research/validation](research/validation). See the [limitations](research/docs/LIMITATIONS.md) before interpreting these retrospective comparisons as operational forecasts.

## Reference website

The existing [ERCOT project context web](ERCOT%20project%20context%20web/README.md) remains a separate tool for exploring the relationships among research questions, figures and conclusions. Its code, assets and deployed entry point are unchanged by this submission organization.

## Before submitting

Use the [Milestone 3 submission checklist](research/docs/SUBMISSION_CHECKLIST.md). Only one team submission is required. The provided instructions say Sunday of Week 8 at 11:59 PM; this repository does not infer a calendar date or override the course portal's deadline.
