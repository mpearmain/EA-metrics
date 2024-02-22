import json
import polars as pl

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

def json2polars(json_data):
    # Lists to hold data
    project_names = []
    repo_names = []
    languages = []
    byte_counts = []

    # Iterate over projects and repositories
    for project_name, repos in json_data.items():
        for repo_name, languages_data in repos.items():
            for language, byte_count in languages_data.items():
                # Append project, repository, language, and byte count to lists
                project_names.append(project_name)
                repo_names.append(repo_name)
                languages.append(language)
                byte_counts.append(byte_count)

    # Create a Polars DataFrame from the lists
    df = pl.DataFrame({
        'Project': project_names,
        'Repository': repo_names,
        'Language': languages,
        'ByteCount': byte_counts
    })

    return df
