# Notebook guide

**Final submitted visualization source:** [Matthew’s complete final notebook](../notebooks/originals/DSC450_ERCOT_Full_Visualization_Hybrid_model.ipynb). This user-designated version is preserved exactly as supplied, with 104 cells and all saved outputs. It was format/syntax checked, not rerun or condensed in this update. The numbered notebooks below remain separate repository adaptations and reproduction tools.

| Notebook | Responsibility and source | Execution status / requirements |
|---|---|---|
| 01_data_wrangling.ipynb | Sarah's EIA-930 cleaning and feature construction; original 47-cell notebook preserved. | Repository paths added. Not executed: original eia930_erco_hourly.csv is missing. The supplied cleaned CSV is included for downstream analysis. |
| 02_model_training.ipynb | Andrea's 98-cell statistical/boosting-model workflow. | Repository paths added; supplied inputs protected from overwrite. Syntax checked, not retrained. Optional model dependencies and potentially expensive rolling fits. Predates the hybrid export. |
| 03_visualization.ipynb | Full 102-cell hybrid visualization source, with the F09 label correction. | Repository paths replace the interactive file picker. Original F20 retained, additional colored opposite-sign version appended. Restart-and-run-all is verified; see validation results. |
| 04_presentation_research.ipynb | Portable extraction of the storyboard research calculations. | Restart-and-run-all is verified from the two frozen CSVs. Reconciles the shared sample, peak hours, hybrid arithmetic and exact July case, and recreates R11P/R12P. No Studio S rebuild. |

## Reproduce the evaluated results

From the repository root, install `research/requirements.txt`, then run `python research/tools/run_notebooks.py`. This executes 03 then 04 and saves their executed outputs back into the working notebooks. Original notebook bytes under `notebooks/originals` are untouched.

Python 3.12 was used for the recorded validation. Each analysis notebook ran in a fresh socket-free IPython subprocess with sequential cell execution and saved outputs. A Jupyter server/kernel could not be launched in this environment, so that specific acceptance test is not claimed. The notebooks remain standard Jupyter notebooks. Exact package versions and source hashes are recorded in validation. Generated figures are in `figures/full_visualization`, `figures/error_directions` and `figures/storyboard`. Temporary tables and build outputs go to `outputs` and are ignored by Git.

## Optional historical cleaning and training

The original raw EIA extract is not supplied. Obtain that original snapshot as `research/data/eia930_erco_hourly.csv` before running 01. Do not substitute the cleaned CSV and call it raw data. Notebook 01 writes its regenerated cleaned output to `research/outputs`, protecting the frozen input in `research/data`.

For 02, install `research/requirements-models.txt`. The original source reads cleaned data and merged observed-weather data. Its source is preserved for method inspection; rerunning its full training sequence has not been certified in this submission pass. Generated prediction exports go to `research/outputs`, not over the supplied prediction CSV. No failed static SARIMA prediction trace is invented.

The original Studio S asset-build notebook is preserved in `notebooks/originals/DSC450_ERCOT_Storyboard_Visuals.ipynb` as historical source. It requires the earlier complete storyboard bundle. The portable 04 notebook extracts the scientific part of that workflow for this repository.
