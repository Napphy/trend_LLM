import os
os.environ["HF_HOME"] = "D:\\HuggingFaceCache"
import dotenv
from transformers import pipeline
from kb_logic import get_project_contact

# Load environment variables
dotenv.load_dotenv()



# Initialize the question-answering pipeline
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def parse_input(user_input, kb_file_path="datas/projects_kb.json"):
    """
    Parse the user input to extract the project name and context.

    Args:
        user_input (str): The user input containing the question and project name.
        kb_file_path (str): Path to the knowledge base file.

    Returns:
        tuple: Extracted project name and context.
    """
    project_name = user_input.split()[-1]
    context = "What is the status of abc1234fefdcbac3cddaefXXXxxXXXxxxXXxX"

    # Debugging
    print("Context retrieved: ", context)

    if "Sorry" in context:
        return None, context

    return project_name, context

def answer_combined_input(user_input, kb_file_path="datas/projects_kb.json"):
    project_name, context = parse_input(user_input, kb_file_path)

    if context.startswith("Sorry"):
        return context 

    # Use the question-answering pipeline
    try:
        response = qa_pipeline({"question": user_input, "context": context})

        if not response.get("answer"):
            return "I'm sorry, I couldn't find an answer to your question."

        return response["answer"]
    except Exception as e:
        return f"Error occurred while processing the question: {e}"

if __name__ == "__main__":
    user_input = input("Enter your question and project name: ")
    answer = answer_combined_input(user_input)
    print(answer)
