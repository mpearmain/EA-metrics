import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable

import pandas as pd
from github import Github, Repository

"""
Example
from repo_crawler import RepoCrawler

# Initialize the RepoCrawler with your GitHub access token
access_token = "your_github_access_token"  # Replace with your actual GitHub access token
crawler = RepoCrawler(access_token=your_access_token)

owners = ['Apache']
repos = crawler.get_repos_by_owner(owners) 

# Specify methods to call and properties to access
repo_methods = {'get_languages': None}
repo_properties = ['stargazers_count']

# Fetch attributes
repo_attributes = crawler.get_attributes(repos=repos[0:10], repo_methods=repo_methods, repo_properties=repo_properties)

print(repo_attributes)

{'Apache/.github': {'get_languages': {}, 'stargazers_count': 11},
 'Apache/abdera': {'get_languages': {'Java': 634197, 'XSLT': 535},
                   'stargazers_count': 18},
 'Apache/accumulo': {'get_languages': {'C': 2438,
                                       'C++': 37322,
                                       'CSS': 7725,
                                       'FreeMarker': 59797,
                                       'HTML': 5505,
                                       'Java': 12970219,
                                       'JavaScript': 87293,
                                       'Makefile': 2873,
                                       'Shell': 82862,
                                       'Thrift': 47298},
                     'stargazers_count': 1046},
 'Apache/accumulo-access': {'get_languages': {'ANTLR': 5230,
                                              'Java': 112567,
                                              'Shell': 23506},
                            'stargazers_count': 4},
 'Apache/accumulo-bsp': {'get_languages': {'Java': 27574},
                         'stargazers_count': 5},
 'Apache/accumulo-classloaders': {'get_languages': {'Java': 92012,
                                                    'Shell': 3248},
                                  'stargazers_count': 3},
 'Apache/accumulo-docker': {'get_languages': {'Dockerfile': 4425,
                                              'Shell': 1778},
                            'stargazers_count': 18},
 'Apache/accumulo-examples': {'get_languages': {'Java': 333228, 'Shell': 5414},
                              'stargazers_count': 34},
 'Apache/accumulo-instamo-archetype': {'get_languages': {'Java': 4717},
                                       'stargazers_count': 2},
 'Apache/accumulo-maven-plugin': {'get_languages': {'Groovy': 1396,
                                                    'Java': 16626,
                                                    'Shell': 22513},
                                  'stargazers_count': 5}}
"""


class RepoCrawler:
    """
    A crawler for GitHub repositories to retrieve and output various information.

    Attributes:
        access_token (str): Personal GitHub access token for authentication.
        github (Github): Instance of Github class from PyGithub for API interactions.

    Methods:
        get_repo(repo_str): Retrieves a specific repository based on its full name.
        get_attributes(repos, **kwargs): Fetches specified attributes for a list of repositories.
        output_results(results, path, output_format): Outputs the fetched attributes to a file in the specified format.
    """

    def __init__(self, access_token: str) -> None:
        """
        Initializes the crawler with a GitHub access token.
        """
        self.access_token = access_token
        self.github = Github(self.access_token)

    def get_repos_by_owner(self, owners: List[str]) -> List[str]:
        all_repos = []
        for owner in owners:
            user = self.github.get_user(owner)
            for repo in user.get_repos():
                all_repos.append(f"{owner}/{repo.name}")
        return all_repos

    def get_repo(self, repo_str: str) -> Repository.Repository:
        """
        Retrieves the GitHub repository object for a given repository string.
        """
        return self.github.get_repo(repo_str)

    def get_attributes(self, repos: List[str], repo_methods: Dict[Callable, Any] = None,
                       repo_properties: List[str] = None) -> Dict[str, Any]:
        results = {}
        for repo_str in repos:
            repo = self.get_repo(repo_str)
            repo_data = {}

            # Handle method calls with optional arguments
            if repo_methods:
                for method, args in repo_methods.items():
                    if hasattr(repo, method):
                        repo_method = getattr(repo, method)
                        if callable(repo_method):
                            try:
                                repo_data[method] = repo_method(**args) if args else repo_method()
                            except TypeError as e:
                                print(f"Error calling {method} with args {args}: {e}")

            # Handle direct property access
            if repo_properties:
                for prop in repo_properties:
                    if hasattr(repo, prop):
                        repo_data[prop] = getattr(repo, prop)

            results[repo_str] = repo_data

        return results

    @staticmethod
    def output_results(results: Dict[str, Any], path: str, output_format: 'OutputFormat') -> None:
        """
        Outputs the fetched repository attributes to a specified path in the given format.
        """
        output_format.output(results, path)


class OutputFormat(ABC):
    """Abstract base class for output formats."""

    @abstractmethod
    def output(self, results: Dict[str, Any], path: str = None) -> None:
        pass


class JsonOutputStrategy(OutputFormat):
    """
    Outputs data in JSON format.
    """

    def output(self, results: Dict[str, Any], path: str = None) -> None:
        with open(path, 'w') as f:
            json.dump(results, f, indent=2)


class PandasOutputStrategy(OutputFormat):
    """Outputs data as a pandas DataFrame, dynamically handling attributes."""

    def output(self, results: Dict[str, Any], path: str = None) -> pd.DataFrame:
        """Convert a dictionary with repository details into a pandas DataFrame dynamically.

        This method processes a dictionary with a structure of {Owner/Repo: {Attribute: Value}}.
        It dynamically generates DataFrame rows based on the keys and values present in the
        dictionary, accommodating any structure without requiring code changes for new variables.

        Args:
            results (dict): The dictionary to convert, with keys as "{Owner}/{Repository}" and
                            dynamic values for various attributes.
            path (str, optional): If provided, the path to save the DataFrame as a CSV file.

        Returns:
            pandas.DataFrame: A DataFrame created dynamically from the dictionary's structure.
        """
        # List to hold each row (dictionary) of data for the DataFrame
        data_rows = []

        for full_repo_name, repo_details in results.items():
            owner, repo_name = full_repo_name.split('/')
            if repo_name == '.github':  # Skip .github repositories
                continue

            # Direct attributes that are not dictionaries (will be shared across rows for the same repo)
            shared_attributes = {k: v for k, v in repo_details.items() if not isinstance(v, dict)}
            shared_attributes.update({'Owner': owner, 'Repository': repo_name})

            # Process nested dictionaries
            nested_attributes_exist = any(isinstance(v, dict) for v in repo_details.values())
            if nested_attributes_exist:
                for attribute, nested_values in repo_details.items():
                    if isinstance(nested_values, dict):
                        for nested_key, nested_value in nested_values.items():
                            row = shared_attributes.copy()
                            row.update({attribute: nested_key, 'Value': nested_value})
                            data_rows.append(row)
            else:
                # If there are no nested dictionaries, add the shared attributes directly
                data_rows.append(shared_attributes)

        df = pd.DataFrame(data_rows)
        # Reordering columns to ensure Owner and Repository are first
        cols = ['Owner', 'Repository'] + [col for col in df.columns if col not in ['Owner', 'Repository']]
        df = df[cols]
        if path:  # Optionally save to CSV
            df.to_csv(path, index=False)

        return df