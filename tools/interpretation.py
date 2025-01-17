import json
import os
from dotenv import load_dotenv
from transformers import tool
from huggingface_hub import InferenceClient

load_dotenv()

inferecence_api = os.getenv("HF_INFERENCE_KEY")

client = InferenceClient(api_key=inferecence_api)

@tool
def interpret_scan_result(scan_result: str, user_query: str) -> str:
    """
    A tool to interpret scan results using Hugging Face's Zephyr-7B-beta model.

    Args:
        scan_result: The JSON string representing the scan result.
        user_query: The string of text representing the user's query.

    Returns:
        str: The interpreted result from the model or an error message.
    """
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. You will provide interpretation for the following scan result based on the User Query."
            },
            {
                "role": "user",
                "content": f"Scan Result: {scan_result} \n User Query:{user_query}"
            }
        ]

        completion = client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-beta",
            messages=messages,
            max_tokens=1000
        )

        return completion.choices[0].message["content"]
    except Exception as e:
        return f"An error occurred: {str(e)}"