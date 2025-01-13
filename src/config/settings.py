import os
from pathlib import Path

# Get project root directory
ROOT_DIR = Path(__file__).parent.parent.parent

# Define common paths
INPUT_DIR = os.path.join(ROOT_DIR, "data", "input")
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "output")

def load_config():
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "input_dir": INPUT_DIR,
        "output_dir": OUTPUT_DIR,
        "input_file": os.getenv("INPUT_FILE", "all-question-papers.txt")
    }
    return config 