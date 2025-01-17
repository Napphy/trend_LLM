from transformers import tool
import re

@tool
def extract_sha1(text: str) -> str:
    """
    Extracts a single SHA1 hash (40-character hexadecimal string) from the input text.
    Returns the hash if found; otherwise, returns a message indicating no hash was found.

    Args:
        text: The input string containing a potential SHA1 hash.
    
    Returns:
        str: The extracted SHA1 hash, or a message if no hash is found.
    """
    sha1_pattern = r'\b[a-fA-F0-9]{40}\b'
    match = re.search(sha1_pattern, text)
    if match:
        return match.group(0)
    else:
        return "No valid SHA1 hash found in the input."

