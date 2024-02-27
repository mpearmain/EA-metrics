import json
import pandas as pd

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