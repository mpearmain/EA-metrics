# EA-Tribal-Knowledge-Analysis

## Overview

This repository demonstrates the use of multilevel (hierarchical) Bayesian modeling to analyze and mitigate tribal knowledge within an organization's codebase. By examining the distribution of programming languages across repositories and projects, we aim to identify areas where knowledge may be overly concentrated or at risk.

## Contents

- `generate_dummy_data.py`: A script to create dummy data resembling GitHub's repository language statistics.
- `tribal_knowledge_model.py`: A script that constructs a Bayesian hierarchical model to analyze the dummy data, aiming to identify tribal knowledge patterns.
- `data/`: Directory to store generated dummy data and any other data files used by the analysis script.

## Getting Started

1. Ensure you have Python installed along with the necessary libraries: `pandas`, `numpy`, `pymc3`, and `matplotlib`.
2. Run `generate_dummy_data.py` to generate the dummy data.
3. Execute `tribal_knowledge_model.py` to build the model and visualize the results.

## Usage

### Generating Dummy Data

```bash
python generate_dummy_data.py
