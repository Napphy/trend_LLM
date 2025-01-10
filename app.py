from flask import Flask, render_template, request, jsonify, Response
import requests
from kb_logic import get_project_contact, add_project_to_kb
import json

app = Flask(__name__)

# Llama model configuration
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def generate_response(prompt):
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True  # If true, responses will be in chunks
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=data, stream=True)
        response.raise_for_status()

        def generate():
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    try:
                        json_chunk = json.loads(chunk)
                        yield json_chunk.get("response", "") + '\n'
                    except json.JSONDecodeError:
                        pass  
        return Response(generate(), content_type='application/json')
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("message")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    project_name = extract_project_name(user_query)
    project_info = get_project_contact(project_name)

    prompt = (
        f"You are an assistant for project management. "
        f"Provide detailed and helpful responses to questions about projects. "
        f"Here is relevant project information:\n\n{project_info}\n\n"
        f"User Query: {user_query}"
    )

    return generate_response(prompt)

@app.route("/add_project", methods=["POST"])
def add_project():
    project_data = request.json  # Expecting JSON input for the new project
    if not project_data:
        return jsonify({"error": "No project data provided"}), 400

    result = add_project_to_kb(project_data)
    return jsonify({"message": result})


def extract_project_name(user_query):
    return user_query.split(" ")[-1]  # Assume the project name is the last word

if __name__ == "__main__":
    app.run(debug=True)
