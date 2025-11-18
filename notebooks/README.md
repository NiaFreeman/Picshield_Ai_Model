# Notebooks Directory

This directory is for Jupyter notebooks used in development and exploration.

## What to Put Here

- Exploratory data analysis (EDA)
- Model prototyping
- Visualization notebooks
- Experiment logs
- Tutorial notebooks

## Example Structure

```
notebooks/
├── 01_data_exploration.ipynb
├── 02_model_prototyping.ipynb
├── 03_results_visualization.ipynb
└── experiments/
    ├── experiment_1.ipynb
    └── experiment_2.ipynb
```

## Best Practices

- Clear outputs before committing (to reduce file size)
- Use descriptive names with numbers for order
- Document your findings within the notebook
- Keep notebooks focused on one topic
- Consider using Jupyter Book for documentation

## Clearing Outputs

```bash
# Clear all outputs before committing
jupyter nbconvert --clear-output --inplace notebook.ipynb

# Or use nbstripout tool
pip install nbstripout
nbstripout notebook.ipynb
```
