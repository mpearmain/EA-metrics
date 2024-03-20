# Simple script to write cypher statements from dummy data

import pandas as pd

# Load the CSV file into a DataFrame
file_path = '../data/dummy_data.csv'  # Adjust to the path of your CSV file
df = pd.read_csv(file_path)

# Open a file to write the Cypher statements
cypher_file_path = '../data/output_cypher_file.cypher'  # Adjust to where you want to save the Cypher file

with open(cypher_file_path, 'w') as cypher_file:
    for _, row in df.iterrows():
        # Extract the simplified repository name by removing the project prefix
        simplified_repo_name = '_'.join(row['Project_Repo'].split('_')[2:])

        # Generate Cypher statement
        cypher_stmt = f"""
MERGE (p:Project {{name: '{row['Project']}'}})
MERGE (r:Repository {{name: '{row['Project_Repo']}'}})
ON CREATE SET r.displayName = '{simplified_repo_name}'
MERGE (l:Language {{name: '{row['Language']}'}})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = {int(row['ByteCount'])};
"""
        cypher_file.write(cypher_stmt + "\n")  # Add a newline for readability between statements

print(f"Cypher statements written to {cypher_file_path}")