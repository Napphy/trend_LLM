from transformers import pipeline
from kb_logic import get_project_contact

model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def parse_input(user_input, kb_file_path="datas/projects_kb.json"):
    """
    Parse the user input to extract the project name and question.

    Args:
        user_input (str): The combined question and project name.
        kb_file_path (str): Path to the knowledge base file.

    Returns:
        tuple: Extracted project name, refined question, and context.
    """
    # Extract the project name (assume it's the last word)
    project_name = user_input.split()[-1]

    # Refine the question by removing the project name
    refined_question = " ".join(user_input.split()[:-1])

    context = get_project_contact(project_name, kb_file=kb_file_path)
    if "Sorry" in context:
        return None, None, context

    return project_name, refined_question, context

def answer_combined_input(user_input, kb_file_path="datas/projects_kb.json"):
    """
    Answer a question based on the combined input containing the project name and query.

    Args:
        user_input (str): The combined question and project name.
        kb_file_path (str): Path to the knowledge base file.

    Returns:
        str: Answer to the question or an error message.
    """
    project_name, question, context = parse_input(user_input, kb_file_path)

    if context.startswith("Sorry"):
        return context  # Return an error message if the project isn't found

    QA_input = {
        'question': question,
        'context': context,
    }
    res = nlp(QA_input)
    return res['answer']

if __name__ == "__main__":
    user_input = input("Enter your question and project name: ")

    answer = answer_combined_input(user_input)
    print(answer)
