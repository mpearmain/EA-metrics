"""
This script will generate dummy data similar to what you might pull from GitHub's REST API for repository languages.
https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repository-languages

GitHub CLI api
https://cli.github.com/manual/gh_api

gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /repos/OWNER/REPO/languages

Example Response:
{
  "C": 78769,
  "Python": 7769
}

Inside the `generate_dummy_data` function we use a gamma distribution to select the number of languages per repo
for ease of parameter adjustment you can visualise what they look like here:
https://homepage.divms.uiowa.edu/~mbognar/applets/gamma.html

"""
import json
import numpy as np
import random
from typing import Dict, List, Any
from scipy.stats import gamma
import os

# Set seed for reproducibility
np.random.seed(42)

# Extended set of languages with top-level prominence (percentage)
languages_prominence = {
    'Python': 13.70, 'JavaScript': 12.79, 'Java': 11.87, 'C#': 4.57, 'PHP': 5.48, 'C++': 5.48, 'TypeScript': 4.57,
    'Ruby': 3.65, 'Swift': 2.74, 'Kotlin': 2.74, 'Go': 2.74, 'Rust': 1.83, 'Scala': 1.83, 'Perl': 0.46, 'Lua': 0.46,
    'Haskell': 0.46, 'Clojure': 0.46, 'Elixir': 0.46, 'Dart': 0.46, 'Groovy': 0.46, 'Objective-C': 0.46, 'Bash': 4.57,
    'PowerShell': 0.46, 'Erlang': 0.46, 'Julia': 0.46, 'Fortran': 0.46, 'R': 0.46, 'MATLAB': 0.46, 'VBA': 0.46,
    'SQL': 6.39, 'HTML': 1.83, 'CSS': 1.83, '.NET': 2.74, 'Rails': 0.46, 'Flutter': 0.46, 'Octave': 0.46, 'F#': 0.46}

"""
Positive Affinities: Represent languages that commonly co-occur within the same projects or repositories, often due to 
    complementary use cases, shared ecosystems, or common development practices. For example, TypeScript has a high 
    positive affinity with JavaScript due to its nature as a superset of JavaScript, and it's commonly used together 
    with HTML and CSS in web development.
Negative Affinities: Indicate languages less likely to be found together within the same repositories, possibly due to 
    overlapping use cases where one language is typically chosen over the other. For example, Python and Java have a 
    negative affinity, reflecting their distinct and often separate ecosystems.
"""

language_affinities = {
    'Python': {'Bash': 0.4, 'R': 0.2, 'JavaScript': -0.2, 'Java': -0.5, 'Lua': -0.6, 'Objective-C': -0.5},
    'JavaScript': {'TypeScript': 0.5, 'HTML': 0.4, 'CSS': 0.4, 'Python': -0.2, 'Java': -0.4},
    'Java': {'Kotlin': 0.4, 'Scala': 0.3, 'Groovy': 0.3, 'Python': -0.5, 'JavaScript': -0.4},
    'C#': {'.NET': 0.5, 'F#': 0.3, 'PowerShell': 0.2, 'Java': -0.4},
    'PHP': {'JavaScript': 0.3, 'HTML': 0.3, 'CSS': 0.3, 'Python': -0.3},
    'C++': {'C': 0.4, 'Python': 0.2, 'Java': -0.3},
    'TypeScript': {'JavaScript': 0.5, 'HTML': 0.4, 'CSS': 0.4},
    'Ruby': {'Rails': 0.4, 'JavaScript': 0.2, 'Java': -0.3},
    'Swift': {'Objective-C': 0.3, 'C++': -0.2, 'Python': -0.2},
    'Kotlin': {'Java': 0.4, 'Scala': 0.3, 'Groovy': 0.2},
    'Go': {'C': 0.2, 'Python': 0.1, 'Java': -0.2},
    'Rust': {'C': 0.3, 'C++': 0.3, 'Python': 0.1},
    'Scala': {'Java': 0.3, 'Kotlin': 0.3, 'Groovy': 0.2},
    'Perl': {'Python': 0.2, 'Bash': 0.3, 'R': -0.2},
    'Lua': {'C': 0.3, 'Python': 0.1, 'Java': -0.2},
    'Haskell': {'Scala': 0.2, 'Erlang': 0.1, 'Python': -0.1},
    'Clojure': {'Java': 0.3, 'Scala': 0.2, 'Kotlin': 0.1},
    'Elixir': {'Erlang': 0.4, 'Ruby': 0.2, 'Python': -0.1},
    'Dart': {'Flutter': 0.5, 'JavaScript': 0.1, 'Java': -0.2},
    'Groovy': {'Java': 0.3, 'Scala': 0.2, 'Kotlin': 0.2},
    'Objective-C': {'Swift': 0.3, 'C++': -0.2, 'Python': -0.5},
    'Bash': {'Python': 0.4, 'Perl': 0.3, 'PowerShell': -0.3},
    'PowerShell': {'C#': 0.3, 'Bash': -0.3, '.NET': 0.4},
    'Erlang': {'Elixir': 0.4, 'Scala': 0.1, 'Java': -0.2},
    'Julia': {'Python': 0.3, 'R': 0.4, 'Matlab': 0.3},
    'Fortran': {'C': 0.2, 'Matlab': 0.3, 'Python': -0.4, 'Java': -0.4},
    'R': {'Python': 0.3, 'Julia': 0.4, 'Matlab': 0.3},
    'MATLAB': {'Octave': 0.4, 'Python': 0.2, 'R': 0.3},
    'VBA': {'SQL': 0.3, 'Python': -0.2, 'Java': -0.3},
    'SQL': {'Python': 0.2, 'Java': 0.1, 'PHP': 0.3},
    'HTML': {'CSS': 0.8, 'JavaScript': 0.8},
    'CSS': {'HTML': 0.8, 'JavaScript': 0.8},
    '.NET': {'C#': 0.5, 'F#': 0.3, 'PowerShell': 0.4},
    'Rails': {'Ruby': 0.4},
    'Flutter': {'Dart': 0.5},
    'Octave': {'MATLAB': 0.4},
    'F#': {'C#': 0.3, '.NET': 0.3}
}


def adjust_probabilities(selected_lang: str, base_probs: Dict[str, float], affinities: Dict[str, Dict[str, float]]) -> \
        Dict[str, float]:
    """
    Adjusts the base probabilities for selecting programming languages in a repository, based on the affinities with a
    recently selected language.

    This function modifies the likelihood of selecting each programming language for inclusion in a repository's
    technology stack.
    It increases or decreases these probabilities to reflect how certain languages are more or less likely to be used
    together, based on predefined affinities.

    Parameters:
    - selected_lang (str): The programming language that has been selected most recently for the repository.
    - base_probs (Dict[str, float]): Initial probabilities for selecting each programming language, before considering
                                     any affinities. Each language is a key, and its base selection probability is the
                                     value.
    - affinities (Dict[str, Dict[str, float]]): A nested dictionary where each key is a programming language, and the
                                                value is another dictionary mapping other languages to affinity scores.
                                                Positive scores increase the likelihood of co-selection, while negative
                                                scores decrease it.

    Returns:
    - adjusted_probs (Dict[str, float]): A dictionary with the same structure as `base_probs`, but with adjusted
                                         probabilities reflecting the selected language's affinities.

    Note:
    - The adjusted probabilities are normalized to ensure they sum to 1, maintaining the validity of a probability
      distribution.
    - Probabilities are constrained to the [0, 1] range to avoid invalid values.
    """
    adjusted_probs = base_probs.copy()
    if selected_lang in affinities:
        for lang, affinity in affinities[selected_lang].items():
            if lang in adjusted_probs:
                # Ensure the adjusted probability stays within the [0, 1] range
                adjusted_probs[lang] = max(min(adjusted_probs[lang] + affinity, 1), 0)

    # Normalize to ensure probabilities sum to 1
    total_prob = sum(adjusted_probs.values())
    adjusted_probs = {lang: prob / total_prob for lang, prob in adjusted_probs.items()}

    return adjusted_probs


def select_languages(languages: List[str], base_probs: Dict[str, float], num_languages: int,
                     affinities: Dict[str, Dict[str, float]]) -> List[str]:
    """
    Selects a set of programming languages for a repository, considering base probabilities and affinities between
    languages.

    This function iteratively selects programming languages to simulate a realistic composition of a repository's
    technology stack, accounting for both the general popularity of languages (base probabilities) and the nuanced
    likelihood of languages being used together (affinities).

    Parameters:
    - languages (List[str]): A list of all possible programming languages available for selection.
    - base_probs (Dict[str, float]): Initial probabilities for each programming language's selection, representing their
                                     general usage frequency.
    - num_languages (int): The total number of programming languages to select for the repository.
    - affinities (Dict[str, Dict[str, float]]): A nested dictionary defining the affinity scores between languages,
                                                influencing probability adjustments.

    Returns:
    - selected_languages (List[str]): A list of programming languages selected for the repository, reflecting a
                                      realistic combination based on base probabilities and affinities.

    Notes:
    - Ensures no language is selected more than once for a single repository.
    - Adjusts and normalizes probabilities after each selection to maintain a valid probability distribution.
    """
    selected_languages = []
    remaining_languages = languages.copy()  # Copy to avoid modifying the original list
    probs = np.array([base_probs[lang] for lang in remaining_languages])

    for _ in range(num_languages):
        normalized_probs = probs / probs.sum()  # Normalize probabilities to sum to 1
        chosen_index = np.random.choice(range(len(remaining_languages)), p=normalized_probs)
        selected_lang = remaining_languages.pop(chosen_index)  # Remove selected language to prevent re-selection
        selected_languages.append(selected_lang)

        # Adjust probabilities for remaining languages based on affinities with the selected language
        if selected_lang in affinities:
            for i, lang in enumerate(remaining_languages):
                if lang in affinities[selected_lang]:
                    # Adjust with affinity, ensuring the probability stays within [0, 1]
                    probs[i] += affinities[selected_lang][lang]
                    probs[i] = max(min(probs[i], 1), 0)

        probs = np.delete(probs, chosen_index)  # Remove the probability of the selected language

    return selected_languages


def generate_dummy_data(num_projects: int = 5, min_repos: int = 3, max_repos: int = 10, mean_languages: int = 4,
                        languages_prominence: Dict[str, int] = None, min_bytes_per_language: int = 10000) -> Dict[
    str, Dict[str, Dict[str, int]]]:
    """
    Generates dummy data simulating the structure and language distribution of repositories within projects,
    akin to data retrieved from a platform like GitHub.

    Parameters:
    - num_projects (int): Number of projects to generate.
    - min_repos (int): Minimum number of repositories per project.
    - max_repos (int): Maximum number of repositories per project.
    - mean_languages (int): Mean number of languages per repository.
    - languages_prominence (Dict[str, int]): Languages and their prominence values.
    - min_bytes_per_language (int): Minimum byte size for any language in a repository.

    Returns:
    - Dict[str, Dict[str, Dict[str, int]]]: Nested dictionary with project names, repository names,
      and programming languages with their corresponding byte sizes.
    """
    projects = {}
    base_probs = {lang: prominence ** 0.5 for lang, prominence in languages_prominence.items()}
    a, scale = 1.2, mean_languages / 1.2  # Parameters for the gamma distribution

    for p in range(1, num_projects + 1):
        project_name = f"Project_{p}"
        projects[project_name] = {}
        for r in range(1, np.random.randint(min_repos, max_repos + 1) + 1):
            repo_name = f"Repo_{r}"
            projects[project_name][repo_name] = {}
            total_languages = len(languages_prominence)
            probabilities = gamma.pdf(np.arange(1, total_languages + 1), a, scale=scale)
            num_languages = np.random.choice(np.arange(1, total_languages + 1), p=probabilities / probabilities.sum())
            selected_languages = select_languages(list(languages_prominence.keys()), base_probs, num_languages,
                                                  {})  # Placeholder for language affinities
            total_repo_bytes = random.randint(500_000, 500_000_000 - min_bytes_per_language * num_languages)
            lang_proportions = np.random.dirichlet([base_probs[lang] for lang in selected_languages]) * (
                        total_repo_bytes - min_bytes_per_language * num_languages)
            lang_bytes = lang_proportions + min_bytes_per_language

            for idx, lang in enumerate(selected_languages):
                projects[project_name][repo_name][lang] = int(lang_bytes[idx])

    return projects


def save_data(data: Dict[Any, Any], directory: str = 'data', filename: str = 'dummy_language_data.json') -> None:
    """
    Saves the given data to a JSON file, creating the directory if it does not exist.

    Parameters:
    - data (Dict[Any, Any]): The data to be saved. It should be a dictionary that can be serialized into JSON.
    - directory (str, optional): The directory where the file will be saved. Defaults to 'data'.
    - filename (str, optional): The name of the file to save the data in. Defaults to 'dummy_language_data.json'.

    Returns:
    - None
    """

    # Construct the full file path
    filepath = os.path.join(directory, filename)

    # Check if the directory exists
    if not os.path.exists(directory):
        # Create the directory if it does not exist
        os.makedirs(directory)

    # Save the data to the specified file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"dummy data generated: saved to {filepath}")


if __name__ == "__main__":
    # mean number of language per repo= 4

    dummy_data = generate_dummy_data(num_projects=50, min_repos=3, max_repos=15, mean_languages=4,
                                     min_bytes_per_language=5_000,  # Desired mean
                                     languages_prominence=languages_prominence)
    save_data(data=dummy_data, directory='data', filename='dummy_language_data.json')
