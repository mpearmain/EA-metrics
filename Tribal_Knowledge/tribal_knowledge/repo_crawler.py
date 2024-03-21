import base64
import requests
from typing import List, Dict, Any
import json
from abc import ABC, abstractmethod

import pandas as pd
from github import Github


class OutputFormat(ABC):
    @abstractmethod
    def transform(self, results: Dict[str, Any]) -> Any:
        """Transforms the results into the desired format."""
        pass


class JsonOutputFormat(OutputFormat):
    def transform(self, results: Dict[str, Any]) -> str:
        """Returns a JSON string representation of the results."""
        return json.dumps(results, indent=2)


class PandasOutputStrategy(OutputFormat):
    """Outputs data as a pandas DataFrame, dynamically handling attributes."""

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
    def fetch_repository_details(self, repos: List[str], details_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetches detailed information for a list of repositories based on specified criteria.
        """
        pass

    @abstractmethod
    def output_results(self, results: Dict[str, Any], output_format: 'OutputFormat') -> None:
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

    def fetch_repository_details(self, projects: List[str], details_spec: Dict[str, str]) -> Dict[str, Any]:
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
                    print(f"Failed to fetch {result_key} for project {project_name}: {response.status_code}")

            results[project_name] = project_details

        return results

    def output_results(self, results: Dict[str, Any], output_format: 'OutputFormat') -> None:
        """
        Outputs the fetched repository attributes using the specified output format.

        Args:
            results (Dict[str, Any]): The fetched repository data.
            output_format ('OutputFormat'): The output format instance to transform and present the data.
        """
        output_format.transform(results)


class GitHubRepositoryInfoExtractor(RepositoryInfoExtractor):
    """
    Extracts repository information from GitHub based on specified identifiers
    and details specifications. Allows for fetching repository names, detailed
    information about each repository, and outputting these details using a specified
    output format.

    Attributes:
        access_token (str): Personal access token for GitHub to authenticate and access data.
        github (Gitub): Instance of the Github class from PyGithub for API interactions.

    Methods:
        fetch_repositories: Fetches repository names based on specified owner identifiers.
        fetch_repository_details: Fetches detailed information for a list of repositories.
        _fetch_properties: Helper method to extract specified properties from a repository.
        _fetch_methods: Helper method to invoke specified methods on a repository.
        output_results: Outputs the fetched repository attributes using the specified output format.

    Example usage:
    from github_repository_info_extractor import GitHubRepositoryInfoExtractor

    # Initialize the extractor with your GitHub access token
    access_token = "your_github_access_token"
    extractor = GitHubRepositoryInfoExtractor(access_token=access_token)

    owners = ['apache']
    repos = extractor.fetch_repositories(identifiers=owners)

    # Details specification for fetching properties and invoking methods
    details_spec = {
        "properties": ["stargazers_count"],  # Direct attributes with no arguments
        "methods": {"get_languages": None}   # Methods, potentially with arguments
    }

    # Fetch repository details for the first 10 repositories
    repo_attributes = extractor.fetch_repository_details(repos=repos[:10], details_spec=details_spec)
    """

    def __init__(self, access_token: str) -> None:
        """
        Initializes the GitHubRepositoryInfoExtractor with a GitHub access token.

        Args:
            access_token (str): Personal access token for GitHub.
        """
        self.access_token = access_token
        self.github = Github(self.access_token)

    def fetch_repositories(self, identifiers: List[str]) -> List[str]:
        """
        Fetches repository names for the given GitHub user or organization identifiers.

        Args:
            identifiers (List[str]): GitHub usernames or organization names.

        Returns:
            List[str]: A list of repository names in the format "owner/repo_name".
        """
        all_repos = []
        for owner in identifiers:
            user = self.github.get_user(owner)
            for repo in user.get_repos():
                all_repos.append(f"{owner}/{repo.name}")
        return all_repos

    def fetch_repository_details(self, repos: List[str], details_spec: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetches detailed information for a list of repositories based on the details specification.

        Args:
            repos (List[str]): A list of repository full names (owner/repo_name).
            details_spec (Dict[str, Any], optional): A dictionary specifying which properties
                                                     and methods to fetch for each repository.

        Returns:
            Dict[str, Any]: A dictionary with repository full names as keys and their detailed
                            information as values.
        """
        if details_spec is None:
            details_spec = {"properties": [], "methods": {}}
        results = {}
        for repo_str in repos:
            repo = self.github.get_repo(repo_str)
            repo_data = {}
            if "properties" in details_spec:
                for prop in details_spec["properties"]:
                    if hasattr(repo, prop):
                        repo_data[prop] = getattr(repo, prop)
            if "methods" in details_spec:
                for method, args in details_spec["methods"].items():
                    if hasattr(repo, method) and callable(getattr(repo, method)):
                        try:
                            repo_data[method] = getattr(repo, method)() if args is None else getattr(repo, method)(
                                *args)
                        except TypeError as e:
                            print(f"Error calling {method} with args {args}: {e}")
            # Add the collected repo_data to the results dictionary under the repository's full name
            results[repo_str] = repo_data
        return results

    @staticmethod
    def _fetch_properties(repo, details_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal method to extract specified properties from a GitHub repository object.

        Args:
            repo: The repository object from which to fetch properties.
            details_spec (Dict[str, Any]): Specifications of properties to fetch. Keys are
                                           property names, and values are ignored (should be None).

        Returns:
            Dict[str, Any]: A dictionary containing the requested properties and their values.
        """
        properties_data = {}
        for attribute in details_spec.keys():
            if details_spec[attribute] is None and hasattr(repo, attribute):
                properties_data[attribute] = getattr(repo, attribute)
        return properties_data

    @staticmethod
    def _fetch_methods(repo, details_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts and invokes specified methods from a GitHub repository object based on the detail specification.

        This static method iterates over the details specification dictionary, where each key represents
        an attribute (method) name to be invoked on the repository object. The values are the arguments
        to be passed to those methods. This method handles both no-argument method calls and methods
        that require arguments, distinguishing them based on the presence of arguments specified in
        the details_spec dictionary.

        Args:
            repo: The repository object from which methods are to be invoked.
            details_spec (Dict[str, Any]): A dictionary specifying which methods to invoke on the repository object.
                                            Keys are method names, and values are the arguments for those methods.
                                            A None value or an empty list/tuple indicates no arguments, while other
                                            values are treated as arguments to be passed to the method.

        Returns:
            Dict[str, Any]: A dictionary containing the results of the invoked methods, with method names as keys
                            and the method invocation results as values.

        Raises:
            TypeError: If an error occurs during method invocation, such as passing incorrect arguments,
                       a TypeError is caught and a message is printed, but the error does not propagate.
        """
        methods_data = {}
        for attribute, args in details_spec.items():
            if hasattr(repo, attribute):
                attr = getattr(repo, attribute)
                if callable(attr):
                    try:
                        # If args is None or an empty collection, call without arguments; otherwise, pass args.
                        methods_data[attribute] = attr() if args in (None, [], ()) else attr(*args)
                    except TypeError as e:
                        print(f"Error calling {attribute} with args {args}: {e}")
        return methods_data

    def output_results(self, results: Dict[str, Any], output_format: 'OutputFormat') -> None:
        """
        Outputs the fetched repository attributes using the specified output format.

        Args:
            results (Dict[str, Any]): The fetched repository data.
            output_format (OutputFormat): The output format to transform and present the data.
        """
        output_format.transform(results)
