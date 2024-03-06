import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data(filepath):
    """Load and parse JSON data from a given filepath.

    Args:
        filepath (str): The path to the JSON file containing the data.

    Returns:
        dict: The parsed JSON data.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


def json2pandas(json_data):
    """Convert JSON data to a pandas DataFrame.

    Args:
        json_data (dict): The JSON data to convert.

    Returns:
        pandas.DataFrame: The converted data as a pandas DataFrame.
    """
    # Initialize lists to hold data
    project_names = []
    repo_names = []
    languages = []
    byte_counts = []

    # Iterate over projects and repositories in the JSON data
    for project_name, repos in json_data.items():
        for repo_name, languages_data in repos.items():
            for language, byte_count in languages_data.items():
                # Append project, repository, language, and byte count to lists
                project_names.append(project_name)
                repo_names.append(repo_name)
                languages.append(language)
                byte_counts.append(byte_count)

    # Create a pandas DataFrame from the lists
    df = pd.DataFrame({
        'Project': project_names,
        'Repository': repo_names,
        'Language': languages,
        'ByteCount': byte_counts
    })

    return df


class LanguagePosteriorAnalysis:
    def __init__(self, df, ppc, repo):
        self.df = df
        self.ppc = ppc
        self.repo = repo
        self.unique_repo = f"{repo['Project']}_{repo['Repository']}"
        self.posterior_samples = ppc.posterior_predictive['language_count_obs'].values

    def get_language_info(self, language):
        query_indexes = self.df[(self.df['Language'] == language) & (self.df['Unique_Repo'] == self.unique_repo)][
            'Repo_Lang_Key_codes']
        if query_indexes.empty:
            return None, None
        query_index = query_indexes.iloc[0]

        language_samples_agg = np.mean(self.posterior_samples[:, :, query_index], axis=0)
        language_observed_byte_count = self.df.loc[self.df['Repo_Lang_Key_codes'] == query_index, 'ByteCount'].iloc[0]

        ci_lower = np.quantile(language_samples_agg, 0.025)
        ci_upper = np.quantile(language_samples_agg, 0.975)

        return language_samples_agg, language_observed_byte_count, ci_lower, ci_upper

    def plot_all_languages_posterior(self):
        languages_in_repo = self.df[self.df['Unique_Repo'] == self.unique_repo]['Language'].unique()
        n_languages = len(languages_in_repo)

        ncols = 2 if n_languages > 1 else 1
        nrows = max(1, (n_languages + ncols - 1) // ncols)

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, nrows * 6))
        if n_languages == 1:
            axes = np.array([axes])
        axes = axes.flatten()

        for i, language in enumerate(languages_in_repo):
            language_info = self.get_language_info(language)
            if language_info[0] is not None:
                self.plot_language(axes[i], *language_info, language)

        # Hide unused subplots
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')

        plt.tight_layout()
        plt.show()

    def plot_language(self, ax, language_samples_agg, language_observed_byte_count, ci_lower, ci_upper, language):
        observed_log_byte_count = np.log(language_observed_byte_count + 1)
        ax.hist(np.log(language_samples_agg + 1), bins=30, alpha=0.7, color='skyblue')
        ax.axvline(x=observed_log_byte_count, color='red', linestyle='--', label='Observed')
        ax.axvline(x=np.log(ci_lower + 1), color='green', linestyle='--', label='95% CI Lower')
        ax.axvline(x=np.log(ci_upper + 1), color='green', linestyle='--', label='95% CI Upper')
        ax.set_title(f'{language}')
        ax.set_xlabel('Log Byte Count')
        ax.set_ylabel('Frequency')
        ax.legend()

    def calculate_outliers(self):
        languages_in_repo = self.df[self.df['Unique_Repo'] == self.unique_repo]['Language'].unique()
        outlier_info = []

        for language in languages_in_repo:
            language_info = self.get_language_info(language)
            if language_info[0] is not None:
                _, language_observed_byte_count, ci_lower, ci_upper = language_info
                observed_log_byte_count = np.log(language_observed_byte_count + 1)
                is_outlier = observed_log_byte_count < np.log(ci_lower + 1) or observed_log_byte_count > np.log(
                    ci_upper + 1)

                outlier_info.append({
                    'language': language,
                    'Observed log byte count': observed_log_byte_count,
                    'Lower CI': np.log(ci_lower + 1),
                    'Upper CI': np.log(ci_upper + 1),
                    'Outlier': is_outlier
                })

        return pd.DataFrame(outlier_info)
