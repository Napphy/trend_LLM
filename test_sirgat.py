from smolagents import CodeAgent, HfApiModel
from tools.hash_extract import extract_sha1
from tools.context_retrieval import retrieve_scan_result
from tools.interpretation import interpret_scan_result
from dotenv import load_dotenv
import os

os.environ["HF_HOME"] = "D:\\HuggingFaceCache"

load_dotenv()
inferecence_api = os.getenv("HF_INFERENCE_KEY")

agent = CodeAgent(
    tools=[extract_sha1, retrieve_scan_result, interpret_scan_result],
    model=HfApiModel(model_id="HuggingFaceH4/zephyr-7b-beta", token=inferecence_api),
    additional_authorized_imports='json'
)

def main():
    # Example query
    query = "What are the scanners found in for 01357986b3e32cfaea73e7ad3e939d86d443e530?"

    structured_input = f"""
    You are a helpful assistant that queries the hash extracted from "{query}" to the retrieve_scan_result tool.
    You will interpret the results by passing the scan results and the query to the interpret_scan_result tool like `interpret_scan_result(scan_result=result, user_query=query)`.
    You add present the scan results as well and the interpretation of the results in the final answer.
                        """
    
    result = agent.run(structured_input)
    
    print(result)

if __name__ == "__main__":
    main()
