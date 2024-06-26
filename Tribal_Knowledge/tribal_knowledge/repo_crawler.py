import base64
import json
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Tuple

import pandas as pd
import requests
from github import Github
from tqdm import tqdm


class OutputFormat(ABC):
    @abstractmethod
    def transform(self, results: Dict[str, Any]) -> Any:
        """Transforms the results into the desired format."""
        pass


class JsonOutputFormat(OutputFormat):
    def transform(self, results: Dict[str, Any]) -> str:
        """Returns a JSON string representation of the results."""
        return json.dumps(results, indent=2)


class PandasOutputFormat(OutputFormat):
    """Outputs data as a pandas DataFrame, dynamically handling attributes."""

    def __init__(self, nested_row: bool = False):
        """
        Args:
            nested_row (bool): If True, generate separate rows for nested dictionaries.
                               If False, return a simpler DataFrame tht ignores nested row variables.
        """
        self.nested_row = nested_row

    def transform(self, results: Dict[str, Any]) -> pd.DataFrame:
        """Convert a dictionary with repository details into a pandas DataFrame dynamically.

        This method processes a dictionary with a structure of {Owner/Repo: {Attribute: Value}}.
        It dynamically generates DataFrame rows based on the keys and values present in the
        dictionary, accommodating any structure without requiring code changes for new variables.

        Args:
            results (dict): The dictionary to convert, with keys as "{Owner}/{Repository}" and
                            dynamic values for various attributes.

        Returns:
            pandas.DataFrame: A DataFrame created dynamically from the dictionary's structure.
        """
        # List to hold each row (dictionary) of data for the DataFrame
        data_rows = []

        for full_repo_name, repo_details in results.items():
            owner, repo_name = full_repo_name.split("/")
            if repo_name == ".github":  # Skip .github repositories
                continue

            shared_attributes = {
                k: v for k, v in repo_details.items() if not isinstance(v, dict)
            }
            shared_attributes.update({"Owner": owner, "Repository": repo_name})

            if self.nested_row:
                # Generate separate rows for nested dictionaries
                nested_attributes_exist = any(isinstance(v, dict) for v in repo_details.values())
                if nested_attributes_exist:
                    for attribute, nested_values in repo_details.items():
                        if isinstance(nested_values, dict):
                            for nested_key, nested_value in nested_values.items():
                                row = shared_attributes.copy()
                                row.update({attribute: nested_key, "Value": nested_value})
                                data_rows.append(row)
                else:
                    data_rows.append(shared_attributes)
            else:
                # Add non-nested attributes directly, skipping the nested rows
                data_rows.append(shared_attributes)

        df = pd.DataFrame(data_rows)
        cols = ["Owner", "Repository"] + [col for col in df.columns if col not in ["Owner", "Repository"]]
        df = df[cols]
        return df


# Define the abstract base class for extracting repository information
class RepositoryInfoExtractor(ABC):
    """
    Abstract base class for extracting repository information from different platforms for example GitHub, Azure Devops,
    Gitlab, AWS CodeCommit...
    """

    @abstractmethod
    def fetch_repositories(self, identifiers: List[str]) -> List[str]:
        """
        Fetches repositories based on given identifiers (owners, organizations, etc.).
        """
        pass

    @abstractmethod
    def fetch_repository_details(
            self, repos: List[str], details_spec: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fetches detailed information for a list of repositories based on specified criteria.
        """
        pass

    @abstractmethod
    def output_results(
            self, results: Dict[str, Any], output_format: "OutputFormat"
    ) -> None:
        """
        Outputs the fetched repository attributes to a specified path in the given format.
        """
        pass


class AzureDevOpsRepositoryInfoExtractor(RepositoryInfoExtractor):
    """
    Extracts repository information from Azure DevOps based on specified organization URL and PAT
    (Personal Access Token).
    Allows for fetching project names, detailed information about each project, and supports custom details
    specification for fetching additional data.

    Attributes:
        org_url (str): The URL of the Azure DevOps organization.
        pat (str): The Personal Access Token for authentication.
        headers (dict): The headers to be included in API requests, including authorization.
        project_api (str): The API endpoint for fetching all projects in the organization.

    Example usage:
    extractor = AzureDevOpsRepositoryInfoExtractor(org_url="https://dev.azure.com/yourOrg", pat="yourPAT")

    projects = extractor.fetch_repositories()
    details_spec = {
       "git/repositories?api-version=6.0": "repos",
       "projectanalysis/languagemetrics", "language"
    }
    project_details = extractor.fetch_repository_details(projects, details_spec)
    """

    def __init__(self, org_url: str, pat: str) -> None:
        """
        Initializes the AzureDevOpsRepositoryInfoExtractor with an organization URL and a PAT.

        Args:
            org_url (str): The URL of the Azure DevOps organization.
            pat (str): The Personal Access Token for authentication.
        """
        self.org_url = org_url
        self.pat = pat
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {base64.b64encode(bytes(':' + self.pat, 'ascii')).decode('ascii')}",
        }
        self.project_api = f"{self.org_url}/_apis/projects?api-version=7.1-preview.4"

    def fetch_repositories(self, identifiers: List[str] = None) -> List[str]:
        """
        Fetches all projects in the Azure DevOps organization.

        Args:
            identifiers (List[str], optional): Currently unused. Included for compatibility with abstract method
            signature.

        Returns:
            List[str]: A list of project names.
        """
        response = requests.get(self.project_api, headers=self.headers)
        if response.status_code == 200:
            projects = response.json()["value"]
            return [project["name"] for project in projects]
        else:
            return []

    def fetch_repository_details(
            self, projects: List[str], details_spec: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Fetches detailed information for a list of Azure DevOps projects based on a details specification.

        The `details_spec` dictionary allows specifying API endpoints and the corresponding keys under which
        to store their results. This approach provides flexibility in determining what data to retrieve.

        Args:
            projects (List[str]): A list of project names to fetch details for.
            details_spec (Dict[str, str]): A dictionary where each key is a partial URL path or complete query
                                           string for an Azure DevOps API endpoint (relative to the project URL),
                                           and each value is the key under which to store the results in the
                                           returned dictionary.

        Returns:
            Dict[str, Any]: Detailed information for each project, with each key being a project name and its value
                            being a dictionary of the requested data as specified in `details_spec`.

        WARNING: The structure below is aimed at POC to enable a test scenario to crawl for data
        The nested for loop and requests.get is a long operation that can time out, exception etc...

        For a more robust implementation using python multithreading inspiration can be taken from the
        `GithubRepositoryInfoExtractor`

        """
        results = {}
        for project_name in projects:
            project_details = {}
            for api_query, result_key in details_spec.items():
                endpoint = f"{self.org_url}/{project_name}/_apis/{api_query}"
                response = requests.get(endpoint, headers=self.headers)
                if response.status_code == 200:
                    project_details[result_key] = response.json()["value"]
                else:
                    print(
                        f"Failed to fetch {result_key} for project {project_name}: {response.status_code}"
                    )

            results[project_name] = project_details

        return results

    def output_results(
            self, results: Dict[str, Any], output_format: "OutputFormat"
    ) -> None:
        """
        Outputs the fetched repository attributes using the specified output format.

        Args:
            results (Dict[str, Any]): The fetched repository data.
            output_format ('OutputFormat'): The output format instance to transform and present the data.
        """
        output_format.transform(results)


class GitHubRepositoryInfoExtractor:
    """
    This class extracts repository information from GitHub, leveraging the PyGithub library for API interactions
    and multithreading to enhance performance by fetching data from multiple repositories in parallel.

    It's designed to query GitHub for a list of repositories based on user or organization identifiers, fetch
    detailed information for each repository, and optionally output these details in a specified format. The
    use of a ThreadPoolExecutor for multithreading enables this class to significantly improve performance
    for fetching large amounts of data without blocking the main execution thread.

    Attributes:
        access_token (str): A personal access token for GitHub used to authenticate and access the GitHub API.
        github (Github): An instance of the Github class from PyGithub, configured with the provided access token.
        executor (ThreadPoolExecutor): A ThreadPoolExecutor instance for managing a pool of threads to execute
                                       API requests concurrently.
        repository_details (Dict[str, Dict[str, Any]]): A dictionary to store detailed information for each
                                                        fetched repository, with repository full names as keys.

    Example Usage:
        with GitHubRepositoryInfoExtractor(access_token="your_github_access_token") as extractor:
            owners = ['apache']
            repos = extractor.fetch_repositories(identifiers=owners)
            details_spec = {
                "properties": ["stargazers_count"],
                "methods": {"get_languages": None}
            }
            repo_attributes = extractor.fetch_repository_details(repos=repos[:10], details_spec=details_spec)

            # Optionally, output the fetched data using a custom format
            extractor.output_results(repo_attributes, SomeOutputFormat())

    The class supports being used as a context manager to ensure proper resource management, particularly
    the graceful shutdown of the ThreadPoolExecutor upon completion. This usage pattern encourages best
    practices in resource management and error handling.
    """

    def __init__(self, access_token: str, max_workers: int = 8) -> None:
        """
        Initializes the GitHubRepositoryInfoExtractor with a GitHub access token and ThreadPoolExecutor for multithreading.

        Args:
            access_token (str): Personal access token for GitHub.
            max_workers (int): Maximum number of threads to use for ThreadPoolExecutor.
        """
        self.access_token = access_token
        self.github = Github(access_token)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.repository_details = {}

    def fetch_repositories(self, identifiers: List[str]) -> List[str]:
        """
        Fetches repository names for given GitHub user or organization identifiers.

        Args:
            identifiers (List[str]): GitHub usernames or organization names.

        Returns:
            List[str]: A list of repository names in the "owner/repo_name" format.
        """
        all_repos = []
        for owner in identifiers:
            user = self.github.get_user(owner)
            all_repos.extend(f"{owner}/{repo.name}" for repo in user.get_repos())
        return all_repos

    def _fetch_details(
            self, repo_full_name: str, details_spec: Dict[str, Any]
    ) -> Tuple[str, dict[Any, Any]]:
        """
        Fetches detailed information for a single repository based on the details specification.

        Args:
            repo_full_name (str): The full name of the repository in the "owner/repo_name" format.
            details_spec (Dict[str, Any]): Specifications for which properties and methods to fetch.

        Returns:
            Dict[str, Any]: A dictionary containing the fetched data.
        """
        repo = self.github.get_repo(repo_full_name)
        repo_data = {}
        # Handle properties
        for prop in details_spec.get("properties", []):
            if hasattr(repo, prop):
                repo_data[prop] = getattr(repo, prop)
        # Handle methods
        for method, args in details_spec.get("methods", {}).items():
            if hasattr(repo, method) and callable(getattr(repo, method)):
                repo_data[method] = (
                    getattr(repo, method)(**args) if args else getattr(repo, method)()
                )

        return repo_full_name, repo_data

    def fetch_repository_details(
            self, repos: List[str], details_spec: Dict[str, Any] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Fetches detailed information for a list of repositories in parallel using multithreading.

        Args:
            repos (List[str]): A list of repository full names (owner/repo_name).
            details_spec (Dict[str, Any], optional): Specification for which properties and methods to fetch.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary with repository full names as keys and their detailed information as values.
        """
        if details_spec is None:
            details_spec = {"properties": [], "methods": {}}

        future_to_repo = {
            self.executor.submit(self._fetch_details, repo, details_spec): repo
            for repo in repos
        }

        # Initialize a tqdm progress bar
        progress = tqdm(
            as_completed(future_to_repo),
            total=len(repos),
            desc="Fetching repository details",
        )

        for future in progress:
            repo, repo_data = future.result()
            self.repository_details[repo] = (
                repo_data  # Store each repo's data in the class attribute
            )
            # Optionally, you can update the progress description dynamically
            # progress.set_description(f"Processed {repo}")

        return self.repository_details

    def close(self) -> None:
        """
        Shuts down the ThreadPoolExecutor, ensuring all resources are freed properly.
        """
        self.executor.shutdown(wait=True)

    def __enter__(self) -> "GitHubRepositoryInfoExtractor":
        """
        Enables the class to be used as a context manager.

        Returns:
            GitHubRepositoryInfoExtractor: The instance of the class itself.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Ensures that resources are cleaned up when exiting the context.

        Args:
            exc_type: Exception type, if any exception was raised within the context.
            exc_val: Exception value, if any exception was raised within the context.
            exc_tb: Traceback object, if any exception was raised within the context.
        """
        self.close()

    def output_results(
            self, results: Dict[str, Any], output_format: "OutputFormat"
    ) -> None:
        """
        Outputs the fetched repository attributes using the specified output format. This is a placeholder method
        meant to be implemented or extended based on specific output requirements (e.g., saving to a file,
        printing to console, transforming into a different data structure).

        Args:
            results (Dict[str, Any]): The fetched repository data.
            output_format (OutputFormat): The output format instance used to transform and present the data.
        """
        output_format.transform(self.repository_details)
