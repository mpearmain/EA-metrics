# EA-Tribal-Knowledge-Analysis

## Overview

This repository showcases a comprehensive approach to understanding and addressing tribal knowledge within an organization's coding practices. Leveraging advanced data generation and Bayesian hierarchical modelling, it simulates realistic scenarios of programming language distribution across various repositories and projects. The aim is to uncover patterns that may indicate knowledge silos or areas where expertise is too concentrated, posing risks to project continuity and team agility.

The data generation process, in particular, employs a nuanced model that accounts for real-world complexities such as language affinities and the skewed distribution of language usage within repositories. This methodological rigour ensures that the generated dummy data closely mirrors actual development environments, providing a solid foundation for subsequent analyses.

## Contents

- `generate_dummy_data.py`: A sophisticated script designed to create realistic dummy data, simulating GitHub's repository language statistics. It incorporates language prominence and affinities to reflect likely language co-occurrences and variations in repository sizes and compositions.
- `tribal_knowledge_model.py`: This script employs Bayesian hierarchical modelling to interpret the generated data, aiming to identify and analyze patterns indicative of tribal knowledge within the codebase.
- `data/`: A directory intended for storing the generated dummy data and any additional data files utilized by the analysis script.

## Getting Started

1. Ensure Python is installed on your system, along with essential libraries such as `pandas`, `numpy`, `pymc3`, and `matplotlib`.
2. Execute `generate_dummy_data.py` to produce the dummy data, closely resembling real-world repository language distributions.
3. Run `tribal_knowledge_model.py` to construct and visualize the Bayesian hierarchical model, leveraging the generated data to uncover insights into tribal knowledge patterns.

## Usage

### Generating Dummy Data

To generate the dummy data, run the following command in your terminal:

```bash
python generate_dummy_data.py
