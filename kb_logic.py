import json
from rapidfuzz import process

# Load the knowledge base
def load_kb(file_path=f"datas/projects_kb.json"):
    with open(file_path, "r") as file:
        return json.load(file)

# Retrieve project information
def get_project_contact(project_name, kb_file=f"datas/projects_kb.json"):
    kb = load_kb(kb_file)
    project_list = kb.keys()

    # Fuzzy match project names
    matched_project, score, index = process.extractOne(project_name, project_list)
    if score < 70:  # Confidence threshold
        return f"Sorry, I couldn't find a close match for '{project_name}' in the database."

    project_info = kb[matched_project]
    return (
        f"Project: {matched_project}\n"
        f"Description: {project_info['description']}\n"
        f"Author: {project_info['author']}\n"
        f"Maintainer: {project_info['maintainer']}\n"
        f"Email: {project_info['email']}\n"
    )
