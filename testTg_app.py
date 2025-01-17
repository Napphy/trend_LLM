from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
# from kb_logic import get_project_contact
from tools.context_retrieval import get_scan_results

load_dotenv()

inference_key = os.getenv("HF_INFERENCE_KEY")

client = InferenceClient(api_key=inference_key)

app = Flask(__name__)

def extract_hash(user_input):
    """Extract the last word from the user input to use as the hash."""
    words = user_input.strip().split()
    return words[-1] if words else ""

@app.route('/')
def index():
    """Render the homepage with a query input form."""
    return render_template('tg_index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    """Handle the user's query and return the assistant's response."""
    user_input = request.form.get('query')
    if not user_input:
        return {"error": "No query provided."}

    hash = extract_hash(user_input)

    project_info = get_scan_results(hash)

    system_message = (
        f"You are an assistant for analyzing and interpreting scan results. "
        f"Provide detailed and helpful responses in English to questions about the hash. "
        f"Here is relevant hash information:\n\n{project_info}\n\n"
    )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input},
    ]

    try:
        completion = client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-beta",
            messages=messages,
            max_tokens=500
        )
        response = completion.choices[0].message["content"]
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(debug=True)
