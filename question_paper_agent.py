import os
import re
from typing import List, Dict
from datetime import datetime
from PyPDF2 import PdfReader
from langchain_openai import OpenAI
from prompt_templates import get_expert_answer_prompt
from config import AppConfig
from models.question import Question
from services.file_service import FileService
from services.question_parser import QuestionParser

class QuestionPaperAgent:
    def __init__(self, *, config: AppConfig):
        self.config = config
        if not self.config.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.llm = OpenAI(api_key=self.config.api_key)
        self.answer_prompt = get_expert_answer_prompt()
        self.file_service = FileService(config.output_dir)
        self.parser = QuestionParser()
        
    def get_questions(self) -> List[Question]:
        """Get parsed questions from input file"""
        content = self.read_input_file()
        return self.parser.parse_questions(content)
        
    def read_input_file(self) -> str:
        """Read content from input file"""
        try:
            with open(self.config.txt_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {self.config.txt_file_path}")
    
    def process_single_question(self, question: Question, question_num: int) -> None:
        """Process and save a single question"""
        try:
            print(f"\nGenerating answer for question {question_num}...")
            question.answer = self.generate_answer(question)
            self.file_service.append_answer(question, question_num)
            print(f"Answer saved to: {self.file_service.output_file}")
        except Exception as e:
            print(f"Error processing question {question_num}: {str(e)}")
            # Still try to save partial results
            if question.answer:
                self.file_service.append_answer(question, question_num)
    
    def generate_answer(self, question: Question) -> str:
        """Generate answer using LLM"""
        prompt = self.answer_prompt.format(
            subject=question.subject,
            section=question.section,
            question=question.question,
            marks=question.marks
        )
        
        # Set max_tokens to ensure we get complete answers
        response = self.llm.invoke(
            prompt,
            temperature=0.7,
            max_tokens=1000,  # Increase token limit
            stop=None  # Don't use any stop sequences
        )
        
        # Clean up the response
        answer = response.strip()
        
        # Ensure the answer ends with a complete sentence
        if not answer.endswith(('.', '!', '?')):
            # If it doesn't end with punctuation, it might be incomplete
            last_sentence_end = max(
                answer.rfind('.'),
                answer.rfind('!'),
                answer.rfind('?')
            )
            if last_sentence_end > 0:
                answer = answer[:last_sentence_end + 1]
        
        return answer

    def process_questions(self) -> str:
        """Process questions and generate answers"""
        # Read and parse questions
        content = self.read_input_file()
        questions = self.parser.parse_questions(content)
        
        print(f"Found {len(questions)} questions to process")
        
        # Generate answers
        results = []
        for i, q in enumerate(questions, 1):
            print(f"Generating answer for question {i}/{len(questions)}...")
            answer = self.generate_answer(q)
            results.append({**q, "answer": answer})
        
        # Save results
        output_file = self.save_results(results)
        return output_file

    def save_results(self, results: List[Dict]) -> str:
        """Save results to output file"""
        if not os.path.exists(self.config.output_dir):
            os.makedirs(self.config.output_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.config.output_dir, f"answers_{timestamp}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("LEGAL EXAM ANSWERS\n")
            f.write("=" * 80 + "\n\n")
            
            # Group questions by subject
            current_subject = None
            
            for result in results:
                # Write subject header if it changes
                if current_subject != result['subject']:
                    current_subject = result['subject']
                    f.write(f"\n{current_subject}\n")
                    f.write("=" * 80 + "\n\n")
                
                # Write section if available
                if result['section']:
                    f.write(f"{result['section']}\n")
                    f.write("-" * 40 + "\n")
                
                # Write question and answer
                f.write(f"Question ({result['marks']} marks):\n")
                f.write(f"{result['question']}\n\n")
                f.write("Answer:\n")
                f.write(f"{result['answer']}\n\n")
                f.write("-" * 80 + "\n\n")
                
        return output_file

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF with improved formatting
        """
        pdf_reader = PdfReader(pdf_path)
        text = ""
        print("\nRaw PDF text extraction:")
        print("=" * 80)
        for page in pdf_reader.pages:
            # Extract text and clean it
            page_text = page.extract_text()
            print(f"\nPage content:")
            print("-" * 40)
            print(page_text)  # Print raw page text before cleaning
            # Remove multiple spaces and normalize newlines
            page_text = ' '.join(page_text.split())
            text += page_text + "\n"
        print("=" * 80)
        return text

    def process_question_paper(self, pdf_path: str, output_dir: str = "output") -> str:
        """
        Process question paper with improved error handling
        """
        try:
            # Extract and clean text from PDF
            print("Extracting text from PDF...")
            text = self.extract_text_from_pdf(pdf_path)
            
            # Parse questions
            print("Parsing questions...")
            questions = self.parser.parse_questions(text)
            
            if not questions:
                raise ValueError("No questions were successfully extracted from the PDF")
            
            print(f"Found {len(questions)} questions")
            
            # Generate answers
            results = []
            for i, q in enumerate(questions, 1):
                print(f"Generating answer for question {i}/{len(questions)}...")
                answer = self.generate_answer(q)
                results.append({
                    "question": q.question,
                    "marks": q.marks,
                    "answer": answer
                })
            
            # Save results
            print("Saving results...")
            output_file = self.save_results(results, output_dir)
            
            return output_file
            
        except Exception as e:
            print(f"Error processing question paper: {str(e)}")
            raise 