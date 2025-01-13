import os
import signal
import sys
from typing import List

from dotenv import load_dotenv

from src.agents.question_paper_agent import QuestionPaperAgent
from src.config.settings import load_config
from src.models.question import Question
from src.services.question_parser import QuestionParser

# Add the config directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "config"))


class GracefulExit:
    def __init__(self):
        self.interrupted = False
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        print("\nReceived interrupt signal. Saving current progress...")
        self.interrupted = True


def display_questions(questions: List[Question]) -> None:
    """Display parsed questions in a formatted way"""
    print("\nParsed Questions:")
    print("=" * 80)

    current_subject = None
    for i, q in enumerate(questions, 1):
        if current_subject != q.subject:
            current_subject = q.subject
            print(f"\n{current_subject}")
            print("=" * 80)

        print(f"\nQ{i}. ({q.marks} marks)")
        print(f"Subject: {q.subject}")
        print(f"Section: {q.section}")
        print(f"Question: {q.question}")
        print("-" * 40)


def get_user_confirmation() -> bool:
    """Get user confirmation to proceed"""
    while True:
        response = input(
            "\nDo you want to generate answers for these questions? (y/n): "
        ).lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        print("Please enter 'y' or 'n'")


def main():
    load_dotenv()
    config = load_config()
    graceful_exit = GracefulExit()

    try:
        agent = QuestionPaperAgent(config)

        try:
            questions = agent.get_questions()
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)

        display_questions(questions)
        print(f"\nTotal questions found: {len(questions)}")

        if get_user_confirmation():
            print(f"\nAnswers will be saved to: {agent.file_service.output_file}")

            for i, question in enumerate(questions, 1):
                if graceful_exit.interrupted:
                    print("\nExiting gracefully. Partial results have been saved.")
                    break

                agent.process_single_question(question, i)

            print("\nProcessing complete. All answers have been saved.")
        else:
            print("\nOperation cancelled by user.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Partial results (if any) have been saved.")
        raise


if __name__ == "__main__":
    main()
