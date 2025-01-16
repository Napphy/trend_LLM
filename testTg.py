import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from kb_logic import get_project_contact

# Load environment variables from .env file
load_dotenv()

# Get the Hugging Face API key from the environment variable
inference_key = os.getenv("HF_INFERENCE_KEY")

# Initialize the Hugging Face Inference Client
client = InferenceClient(api_key=inference_key)

def extract_project_name(user_input):
    """Extract the last word from the user input to use as the project name."""
    words = user_input.strip().split()
    return words[-1] if words else ""

def main():
    print("Welcome to the Project Management Assistant!")

    while True:
        user_input = input("\nPlease enter your query about a project (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Extract the last word as the project name
        project_name = extract_project_name(user_input)

        # Retrieve project information dynamically
        project_info = get_project_contact(project_name)

        # Define the system message with project context
        system_message = (
            f"You are an assistant for project management. "
            f"Provide detailed and helpful responses to questions about projects. "
            f"Here is relevant project information:\n\n{project_info}\n\n"
        )

        # Prepare the conversation context
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ]

        # Generate the response using the Inference Client
        try:
            completion = client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-beta", 
            messages=messages, 
            max_tokens=500
        )
            response = completion.choices[0].message["content"]
            print(f"\nAssistant Response:\n{response}")
        except Exception as e:
            print(f"An error occurred while generating a response: {e}")

if __name__ == "__main__":
    main()
