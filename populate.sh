#!/bin/bash
'''
This is a simple script to run just to populate the new metric idea and be consistent with the other in the repo
its not really designed to do much except create the subfolder using poetry to keep track of dependencies and keep
things a little more tidy and consistent across metric projects.
'''

# Define your metrics here
metrics=("YOUR METRIC IDEA HERE")

# Loop through each metric and create the necessary structure
for metric in "${metrics[@]}"
do
   echo "Creating structure for $metric"

   # Create the directory for the metric
   mkdir -p "$metric"
   cd "$metric"

   # Create a README.md file
   touch README.md
    # Create an __init__.py file to make the directory a Python package
   touch "__init__.py"

   # Convert metric name to lowercase and replace underscores with hyphens for folder and Python file naming
   folder_name=${metric,,}
   folder_name=${folder_name//_/-}

   # Initialize Python project with Poetry, which automatically creates pyproject.toml
   poetry init --name "$folder_name" --dependency numpy --dependency pandas --no-interaction

   # Install the dependencies specified
   poetry install --no-root

   # Create the main Python script for the metric analysis
   echo "# Example script for $metric metric analysis" > "${folder_name}.py"

   # Navigate back to the root directory
   cd ..
done

echo "Structure and initial Python projects created for all metrics."
