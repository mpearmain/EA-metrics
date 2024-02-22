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

def data_prep_with_granularity(json_data):
    # Lists to hold index levels and data
    index = []  # Will contain tuples of (Project, Repository)
    data = []  # Will contain tuples of (Language, ByteCount)

    # Iterate over projects and repositories
    for project_name, repos in json_data.items():
        for repo_name, languages in repos.items():
            for language, byte_count in languages.items():
                # Append project and repository to index list
                index.append((project_name, repo_name))
                # Append language and byte count to data list
                data.append((language, byte_count))

    # Create a MultiIndex from the index list
    multi_index = pd.MultiIndex.from_tuples(index, names=['Project', 'Repository'])

    # Create the DataFrame using the multi-index and data
    df = pd.DataFrame(data, index=multi_index, columns=['Language', 'ByteCount'])

    return df
