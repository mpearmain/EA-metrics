import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from joblib import dump, load


def save_with_joblib(data, filepath):
    """Save data to a file using joblib.

    Args:
        data: The data to save. Can be any Python object joblib can serialize.
        filepath (str): The path to the file where the data will be saved.
    """
    dump(data, filepath)
    print(f"Data successfully saved to {filepath}.")


def load_with_joblib(filepath):
    """Load data from a file saved with joblib.

    Args:
        filepath (str): The path to the file from which to load the data.

    Returns:
        The data loaded from the file.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No file found at {filepath}")

    return load(filepath)


class LanguagePosteriorAnalysis:
    def __init__(self, df, ppc, repo):
        self.df = df
        self.ppc = ppc
        self.repo = repo
        self.unique_repo = f"{repo['Owner']}_{repo['Repository']}"
        self.posterior_samples = ppc.posterior_predictive["language_count_obs"].values

    def get_language_info(self, language):
        query_indexes = self.df[
            (self.df["Language"] == language)
            & (self.df["Unique_Repo"] == self.unique_repo)
            ]["Repo_Lang_Key_codes"]
        if query_indexes.empty:
            return None, None
        query_index = query_indexes.iloc[0]

        language_samples_agg = np.mean(
            self.posterior_samples[:, :, query_index], axis=0
        )
        language_observed_byte_count = self.df.loc[
            self.df["Repo_Lang_Key_codes"] == query_index, "ByteCount"
        ].iloc[0]

        ci_lower = np.quantile(language_samples_agg, 0.025)
        ci_upper = np.quantile(language_samples_agg, 0.975)

        return language_samples_agg, language_observed_byte_count, ci_lower, ci_upper

    def plot_all_languages_posterior(self):
        languages_in_repo = self.df[self.df["Unique_Repo"] == self.unique_repo][
            "Language"
        ].unique()
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
            axes[j].axis("off")

        plt.tight_layout()
        plt.show()

    def plot_language(
            self,
            ax,
            language_samples_agg,
            language_observed_byte_count,
            ci_lower,
            ci_upper,
            language,
    ):
        observed_log_byte_count = np.log(language_observed_byte_count)
        ax.hist(np.log(language_samples_agg + 1), bins=30, alpha=0.7, color="skyblue")
        ax.axvline(
            x=observed_log_byte_count,
            color="red",
            linestyle="--",
            label=f"Observed {observed_log_byte_count:.2f}",
        )
        ax.axvline(
            x=np.log(ci_lower + 1), color="green", linestyle="--", label="95% CI Lower"
        )
        ax.axvline(
            x=np.log(ci_upper + 1), color="green", linestyle="--", label="95% CI Upper"
        )
        ax.set_title(f"{language}")
        ax.set_xlabel("Log Byte Count")
        ax.set_ylabel("Frequency")
        ax.legend()

    def calculate_outliers(self):
        languages_in_repo = self.df[self.df["Unique_Repo"] == self.unique_repo][
            "Language"
        ].unique()
        outlier_info = []

        for language in languages_in_repo:
            language_info = self.get_language_info(language)
            if language_info[0] is not None:
                _, language_observed_byte_count, ci_lower, ci_upper = language_info
                observed_log_byte_count = np.log(language_observed_byte_count + 1)
                is_outlier = observed_log_byte_count < np.log(
                    ci_lower + 1
                ) or observed_log_byte_count > np.log(ci_upper + 1)

                outlier_info.append(
                    {
                        "language": language,
                        "Observed log byte count": observed_log_byte_count,
                        "Lower CI": np.log(ci_lower + 1),
                        "Upper CI": np.log(ci_upper + 1),
                        "Outlier": is_outlier,
                    }
                )

        return pd.DataFrame(outlier_info)
