from flask import Flask, render_template, request, jsonify, Response
import requests
from kb_logic import get_project_contact
import json

app = Flask(__name__)

# Llama model configuration
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Function to generate response from the API with streaming support
def generate_response(prompt):
    # Prepare the data for the request
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True  # If you want streaming, set it to True
    }

    # Send the POST request to the API with streaming enabled
    try:
        response = requests.post(OLLAMA_API_URL, json=data, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Process and yield each chunk of data from the API
        def generate():
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    try:
                        # Parse the chunk to get the response
                        json_chunk = json.loads(chunk)
                        yield json_chunk.get("response", "") + '\n'
                    except json.JSONDecodeError:
                        pass  # Ignore any invalid JSON chunks
        return Response(generate(), content_type='application/json')
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Route for home page
@app.route("/")
def index():
    return render_template("index.html")

# API for chatbot interaction with streaming support
@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("message")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Extract project name and fetch details
    project_name = extract_project_name(user_query)
    project_info = get_project_contact(project_name)

    # Construct prompt for the LLM
    prompt = (
        f"You are an assistant for project management. "
        f"Provide detailed and helpful responses to questions about projects. "
        f"Here is relevant project information:\n\n{project_info}\n\n"
        f"User Query: {user_query}"
    )

    # Query the Llama model with streaming
    return generate_response(prompt)

# Placeholder: Extract project name (basic example)
def extract_project_name(user_query):
    return user_query.split(" ")[-1]  # Assume the project name is the last word

if __name__ == "__main__":
    app.run(debug=True)
