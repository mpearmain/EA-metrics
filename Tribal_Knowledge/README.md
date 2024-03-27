# Tribal Knowledge Project: A Hierarchical Bayesian Approach

## Overview

The Tribal Knowledge Project introduces a data-driven, analytical approach to quantitatively assess and mitigate
technological risks. Leveraging Hierarchical Bayesian Modeling (HBM), this project focuses on dissecting the layers of
risk across repositories, providing insights into maintenance challenges, stability, and the impact of technological
decisions on operational health for consistency and siloed knowledge.

## Key Metrics for Risk Assessment

Our methodology centers around seven critical factors, each chosen for its significance in highlighting potential risks:

- **Time Since Last Commit**: Measures project activity and potential dormancy risks.
- **Age of the Repo**: Reflects the repository's lifecycle stage, from active development to potential legacy status.
- **Commit Frequency (CF)**: Indicates ongoing development efforts and maintenance.
- **Open Issues Ratio (OIR)**: Reveals responsiveness and efficiency in addressing project concerns.
- **Pull Request Resolution Time (PRRT)**: Highlights the development process's efficiency and potential bottlenecks.
- **Total Number of Languages in the Repo**: Points to complexity and potential integration or maintenance challenges.
- **Average Number of Commits per Month**: Offers insights into the development momentum and project vitality.

### Composite Function and Problem-Solving Capability

By mathematically combining these metrics, we create a composite function that assesses risk across multiple dimensions,
enabling prioritisation of mitigation efforts, an early warning system for potential risks, and informed strategic
decision-making.

## Project Structure

- `data`: Contains scripts for data generation and output files for analysis.
- `streamlit`: Hosts the Streamlit application for interactive data visualization.
- `tribal_knowledge`: Core package with scripts for repository crawling and data analysis.

### Key Components

- `.env`: Stores API keys and sensitive configuration details i.e github tokens, azure pat, etc
- `poetry.lock` & `pyproject.toml`: Manage project dependencies.
- `tribal_knowledge.ipynb`: Main Jupyter notebook for project analysis.

## Installation

To set up the project environment:

1. Install Poetry: `pip install poetry`
2. Install dependencies: `poetry install`

## Usage

- **Analysis**: Launch the Jupyter notebook (`tribal_knowledge.ipynb`) to conduct risk analysis.
- **Interactive Visualization**: Run the Streamlit app (`streamlit/app.py`).

## Contributing

We welcome contributions to enhance the project's methodology, data analysis, or visualizations.
Please submit pull requests or report issues via GitHub.