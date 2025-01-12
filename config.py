import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    input_type: str = "txt"  # or "pdf"
    txt_file_path: str = "./input/all-question-papers.txt"
    pdf_file_path: str = None
    output_dir: str = "output"
    api_key: str = None

    def __post_init__(self):
        # Load API key from environment if not provided
        if self.api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY") 