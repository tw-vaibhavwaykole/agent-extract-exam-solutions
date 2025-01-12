import re
from typing import List
from models.question import Question

class QuestionParser:
    def __init__(self):
        # Common patterns for question identification
        self.question_patterns = [
            r'(?:Q\.?\s*)?(\d+)\.?\s*(.*?)(?=(?:Q\.?\s*\d+)|$)',  # Q.1 or 1. format
            r'Question\s+(\d+)[.:]?\s*(.*?)(?=Question\s+\d+|$)',  # "Question 1" format
        ]
        
        # Common patterns for subject identification
        self.subject_indicators = [
            r'###\s*(.*?)\s*(?=###|$)',  # Markdown style
            r'^Subject[:\s]+(.+)$',       # "Subject:" prefix
            r'^[A-Z][A-Za-z\s\-]+(?:Law|Relations|Methods|Rights)',  # Common law subject names
        ]
        
        # Common patterns for section identification
        self.section_patterns = [
            r'\*\*Part[:\s]+([A-Z])[:\s]*(.*?)\*\*',  # **Part A** format
            r'Part[:\s]+([A-Z])[:\s]*(.*?)(?=Part|$)', # Part A format
            r'Section[:\s]+([A-Z])[:\s]*(.*?)(?=Section|$)',  # Section format
        ]

    def _extract_marks(self, text: str) -> int:
        """Extract marks from text using various patterns"""
        marks_patterns = [
            r'\((\d+)\s*marks?\)',  # (10 marks)
            r'\[(\d+)\s*marks?\]',  # [10 marks]
            r'(\d+)\s*marks?',      # 10 marks
        ]
        
        for pattern in marks_patterns:
            if match := re.search(pattern, text, re.IGNORECASE):
                return int(match.group(1))
        
        # Default marks based on common patterns
        if any(indicator in text.lower() for indicator in ['short note', 'brief', 'explain']):
            return 5
        return 12  # Default for longer questions

    def _identify_subject(self, text: str, current_subject: str) -> str:
        """Identify subject from text using various patterns"""
        for pattern in self.subject_indicators:
            if match := re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
                return match.group(1).strip()
        return current_subject

    def _identify_section(self, text: str, current_section: str) -> str:
        """Identify section from text using various patterns"""
        for pattern in self.section_patterns:
            if match := re.search(pattern, text, re.IGNORECASE):
                section_id = match.group(1)
                section_text = match.group(2) if len(match.groups()) > 1 else ""
                return f"Part {section_id}: {section_text}" 

    def generate_answer(self, question_data):
        """
        Generate an answer for a given question using the AI model
        """
        # Format the prompt with question details
        prompt = self.prompt_template.format(
            subject=question_data['subject'],
            section=question_data['section'],
            question=question_data['question'],
            marks=question_data['marks']
        )

        # Get response from AI model
        response = self.ai_client.generate_response(prompt)
        
        # Return the complete answer without any length restrictions
        return response.strip() 

    def parse_questions(self, content: str) -> List[Question]:
        """Parse questions from content and return list of Question objects"""
        questions = []
        current_subject = ""
        current_section = ""
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('### '):
                current_subject = line.replace('### ', '').strip()
                current_subject = current_subject.replace('*', '').strip()
            elif line.startswith('**Part'):
                current_section = line
            elif line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.')):
                question_text = line[line.find('.') + 1:].strip()
                if question_text:
                    marks = 12 if "Part B" in current_section else 4
                    question = Question(
                        subject=current_subject,
                        section=current_section,
                        question=question_text,
                        marks=marks
                    )
                    questions.append(question)
        
        return questions 