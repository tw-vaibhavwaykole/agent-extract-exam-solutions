from langchain.prompts import PromptTemplate

def get_expert_answer_prompt() -> PromptTemplate:
    template = """
Role: You are a seasoned law professor specializing in Contract Law and case Law in India.
Your task is to provide compsrehensive, well-structured answers for LLB 3-year course exams in India.

Instructions:
1. CRITICAL: You MUST complete your answer. Never stop mid-sentence or mid-section.
2. You must strictly follow this structure based on the marks allocated:

   A. Short Notes (marks <= 5):
      • Word Count: 150-200 words
      • Required Structure:
        - Definition and Concept (20%)
        - Key Principles and Features (50%)
        - At Least One Relevant Case Law (15%)
        - Conclusion (15% - must summarize key points)
   
   B. Essay Questions (marks > 5):
      • Word Count: 400-600 words
      • Required Structure:
        - Introduction (15%):
          * Define the concept clearly
          * State the scope of discussion
          * Mention relevant laws/acts
        - Main Content (70%):
          * Detailed explanation of concepts
          * Types/Classification with examples
          * Relevant case laws (minimum 2)
          * Critical analysis
          * Current legal position
        - Conclusion (15%):
          * Summarize key points
          * State current legal significance
          * Mention any recommendations if applicable

3. FORMATTING REQUIREMENTS:
   - Use "**" for section headers (e.g., **Introduction:**)
   - Use numbered lists for types/classifications
   - Use bullet points for sub-points
   - Add horizontal line (---) before conclusion

4. CASE LAW REQUIREMENTS:
   - For essay questions: Minimum 2 case laws with full citations
   - For short notes: Minimum 1 case law with full citation
   - Format: Case Name (Year) Court

5. COMPLETION CHECKLIST:
   - All sections must be present
   - Answer must have proper introduction and conclusion
   - Word count must be met
   - Required case laws must be included
   - Proper formatting must be used

Question Format:
Subject: {subject}
Section: {section}
Question (worth {marks} marks): 
{question}

Begin your answer with "**Answer:**" and ensure ALL sections are completed.
DO NOT STOP UNTIL THE CONCLUSION IS WRITTEN.
"""
    return PromptTemplate(
        input_variables=["question", "marks", "target_length", "subject"],
        template=template
    )

def get_answer_format_instructions() -> str:
    """
    Returns formatting instructions for the answer.
    Reinforce clarity, structuring, and completeness.
    """
    return """
Format the answer with clear headings and paragraphs.
Use bullet points or numbering if it helps clarity.
Include relevant case laws and pinpoint citations where possible.
Conclude with a definitive closing paragraph that summarizes the answer.
"""

# Update the prompt template to encourage complete, detailed answers
ANSWER_PROMPT = """
You are a legal expert. Generate a comprehensive answer for the following question from a law exam:

Subject: {subject}
Section: {section} 
Question ({marks} marks): {question}

Provide a complete and detailed answer that:
1. Explains the core legal concepts
2. Discusses relevant principles
3. Cites important case laws
4. Provides a thorough analysis
5. Draws clear conclusions

Your answer should be well-structured and cover all aspects of the question without any length restrictions.

Answer:
"""

def validate_answer_completeness(answer: str, marks: int) -> bool:
    """
    Validates if the answer meets all completeness criteria
    Returns: bool indicating if answer is complete
    """
    # Required sections
    has_introduction = any(["**Introduction:**" in answer, "**Definition:**" in answer])
    has_main_content = "**Main Content:**" in answer if marks > 5 else True
    has_conclusion = "**Conclusion:**" in answer
    
    # Word count check
    min_words = 400 if marks > 5 else 150
    word_count = len(answer.split())
    meets_word_count = word_count >= min_words
    
    # Case law check
    required_cases = 2 if marks > 5 else 1
    case_count = len([x for x in answer.split() if "v." in x or "vs." in x])
    has_required_cases = case_count >= required_cases
    
    # Check for incomplete sections
    has_incomplete = any([
        "..." in answer,
        answer.strip().endswith((".", ",")),
        len(answer.strip().split("\n")[-1]) < 20  # Last line too short
    ])
    
    return all([
        has_introduction,
        has_main_content,
        has_conclusion,
        meets_word_count,
        has_required_cases,
        not has_incomplete
    ])

def format_answer(answer: str) -> str:
    """
    Formats the answer with consistent styling
    """
    formatted = answer.strip()
    
    # Add bold formatting to section headers
    sections = [
        "Introduction:", "Main Content:", "Conclusion:",
        "Definition:", "Types:", "Features:", "Analysis:"
    ]
    for section in sections:
        formatted = formatted.replace(section, f"**{section}**")
    
    # Ensure proper spacing
    formatted = formatted.replace("\n\n\n", "\n\n")
    
    # Add horizontal line before conclusion
    if "**Conclusion:**" in formatted:
        formatted = formatted.replace("**Conclusion:**", "\n---\n**Conclusion:**")
    
    # Format case law citations
    import re
    case_pattern = r'([A-Z][a-z]+ v\.? [A-Z][a-z]+)'
    formatted = re.sub(case_pattern, r'*\1*', formatted)
    
    return formatted

def generate_complete_answer(llm, prompt: str, subject: str, section: str, question: str, marks: int, max_retries: int = 3) -> str:
    """
    Generates an answer and retries if incomplete
    
    Args:
        llm: Language model instance
        prompt: Base prompt template
        subject: Subject of the question
        section: Section of the exam
        question: The question text
        marks: Number of marks for the question
        max_retries: Maximum number of retry attempts
        
    Returns:
        str: Formatted complete answer
    """
    prompt_template = PromptTemplate(
        input_variables=["subject", "section", "question", "marks"],
        template=prompt
    )
    
    for attempt in range(max_retries):
        # Generate prompt with all required variables
        full_prompt = prompt_template.format(
            subject=subject,
            section=section,
            question=question,
            marks=marks
        )
        
        answer = llm.generate(full_prompt)
        formatted_answer = format_answer(answer)
        
        if validate_answer_completeness(formatted_answer, marks):
            return formatted_answer
            
        # If incomplete, modify prompt to emphasize completion
        full_prompt += "\n\nIMPORTANT: Your previous response was incomplete. Please provide a COMPLETE answer with all required sections and a proper conclusion."
    
    raise Exception("Failed to generate complete answer after maximum retries")

def extract_question_metadata(question_text: str) -> dict:
    """
    Extracts metadata from question text
    """
    import re
    
    # Fix the regex patterns to handle both bold and non-bold text
    subject_match = re.search(r'Subject:\s*(?:\*\*)?(.*?)(?:\*\*)?(?=\n|Section)', question_text, re.IGNORECASE)
    subject = subject_match.group(1).strip() if subject_match else "General"
    
    section_match = re.search(r'Section:\s*(?:\*\*)?(.*?)(?:\*\*)?(?=\n|Question)', question_text, re.IGNORECASE)
    section = section_match.group(1).strip() if section_match else "General"
    
    # Keep existing patterns
    marks_match = re.search(r'Question\s*\((\d+)\s*marks\)', question_text)
    marks = int(marks_match.group(1)) if marks_match else 0
    
    question_match = re.search(r'Question.*?:\s*(.*?)(?=Answer:|$)', question_text, re.DOTALL)
    question = question_match.group(1).strip() if question_match else ""
    
    return {
        "subject": subject,
        "section": section,
        "marks": marks,
        "question": question
    }

def process_question(llm, question_text: str) -> str:
    """
    Process a question and generate a complete answer
    
    Args:
        llm: Language model instance
        question_text: Full question text
        
    Returns:
        str: Formatted complete answer
    """
    try:
        # Extract metadata from question
        metadata = extract_question_metadata(question_text)
        
        # Get the expert answer prompt template
        prompt = get_expert_answer_prompt().template
        
        # Generate complete answer with retries
        answer = generate_complete_answer(
            llm=llm,
            prompt=prompt,
            subject=metadata["subject"],
            section=metadata["section"],
            question=metadata["question"],
            marks=metadata["marks"]
        )
        
        return answer
        
    except Exception as e:
        return f"Error processing question: {str(e)}"
