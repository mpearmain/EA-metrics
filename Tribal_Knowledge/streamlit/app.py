import streamlit as st
import os
from dotenv import load_dotenv
from tribal_knowledge.repo_crawler import RepoCrawler

st.title("GitHub Repository Risk Assessor")

load_dotenv('./.env')
github_token = os.getenv("GITHUB_API_TOKEN")

if github_token:
    st.success("GitHub API token loaded from .env file.")
else:
    github_token = st.text_input("Enter your GitHub access token:", type="password")

owner = st.text_input('Enter the GitHub owner name:')

# Initialize session state for repositories
if 'repositories' not in st.session_state:
    st.session_state['repositories'] = None
    st.session_state['selected_repos'] = None

crawler = RepoCrawler(access_token=github_token)

# Button to fetch repositories
if st.button('Get Repositories by owner', key='get_repos_button') and owner:
    try:
        repos = crawler.get_repos_by_owner([owner])
        st.session_state['repositories'] = repos
        st.success("Repositories fetched successfully.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Use the stored repositories if they exist
if st.session_state['repositories']:
    repos = st.session_state['repositories']
    # Choose selection widget based on the number of repositories
    if len(repos) >= 10:
        if st.checkbox('Select All'):
            default_selection = repos
        else:
            default_selection = []

        st.session_state['selected_repos'] = st.multiselect('Select repositories:', repos, default=default_selection)
    else:
        st.session_state['selected_repos'] = st.selectbox('Select a repository:', [''] + repos)

# Button to analyze selected repositories
if st.button('Select', key='select_repos_button'):
    if st.session_state['selected_repos']:
        st.write(f"Selected repositories for analysis: {st.session_state['selected_repos']}")
        # Perform analysis using the selected repositories
        # E.g., crawler.get_attributes(st.session_state['selected_repos'], ...)
    else:
        st.error("Please select at least one repository for analysis.")

# Inputs for specifying methods and properties
st.subheader("Specify Repository Attributes")
st.write("Enter the repository methods and properties you want to analyze, separated by commas.")
input_methods = st.text_area("Enter methods (e.g., get_contributors, get_languages):")
input_properties = st.text_area("Enter properties (e.g., stargazers_count, forks_count):")

# Session state to store user inputs
if 'repo_methods' not in st.session_state:
    st.session_state['repo_methods'] = {}
if 'repo_properties' not in st.session_state:
    st.session_state['repo_properties'] = []

# Button to analyze selected repositories
if st.button('Get repo information', key='get_repos_info'):
    if st.session_state['selected_repos']:
        # Parse inputs and update session state
        if input_methods:
            method_list = [method.strip() for method in input_methods.split(',')]
            st.session_state['repo_methods'] = {method: None for method in method_list}
        if input_properties:
            st.session_state['repo_properties'] = [prop.strip() for prop in input_properties.split(',')]

        st.write(f"Selected repositories for analysis: {st.session_state['selected_repos']}")
        # Calling get_attributes to fetch data
        try:
            repo_attributes = crawler.get_attributes(
                repos=st.session_state['selected_repos'],
                repo_methods=st.session_state['repo_methods'],
                repo_properties=st.session_state['repo_properties']
            )
            # Assuming the result is a dictionary, you can output it directly. Adjust as needed.
            st.json(repo_attributes)
        except Exception as e:
            st.error(f"An error occurred while fetching repository attributes: {e}")
    else:
        st.error("Please select at least one repository for analysis.")
