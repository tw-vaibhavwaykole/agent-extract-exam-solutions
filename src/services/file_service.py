import os
from datetime import datetime
from typing import List

from src.models.question import Question


class FileService:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.output_file = self._create_output_file()
        self._initialize_output_file()

    def _create_output_file(self) -> str:
        """Create a new output file with timestamp"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"answers_{timestamp}.txt")

    def _initialize_output_file(self) -> None:
        """Initialize the output file with header"""
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("LEGAL EXAM ANSWERS\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

    def append_answer(self, question: Question, question_num: int) -> None:
        """Append a single question and its answer to the file"""
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(f"\nQuestion {question_num}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Subject: {question.subject}\n")
            f.write(f"Section: {question.section}\n")
            f.write(f"Question ({question.marks} marks):\n")
            f.write(f"{question.question}\n\n")
            f.write("Answer:\n")
            f.write(f"{question.answer}\n")
            f.write("-" * 80 + "\n")
            # Flush the file buffer to ensure content is written
            f.flush()
            os.fsync(f.fileno())
