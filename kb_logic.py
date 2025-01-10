import json
from rapidfuzz import process

# Load the knowledge base
def load_kb(file_path=f"datas/projects_kb.json"):
    with open(file_path, "r") as file:
        return json.load(file)

# Save the updated knowledge base
def save_kb(data, file_path=f"datas/projects_kb.json"):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

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

# Add a new project to the knowledge base
def add_project_to_kb(project_data, kb_file=f"datas/projects_kb.json"):
    kb = load_kb(kb_file)
    
    project_name = project_data.get("projectName")
    if project_name in kb:
        return f"Project '{project_name}' already exists in the knowledge base."

    kb[project_name] = {
        "description": project_data.get("description", "No description provided."),
        "author": project_data.get("author", "Unknown"),
        "maintainer": project_data.get("maintainer", "Unknown"),
        "email": project_data.get("email", "Unknown"),
    }
    save_kb(kb, kb_file)
    return f"Project '{project_name}' successfully added to the knowledge base."
