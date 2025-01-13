# LLM Exam Paper Answer Generator

This project is designed to help generate answer papers for questions in LLM exam papers. It uses OpenAI's API for generating comprehensive answers based on provided questions and a structured prompt template. The prompt template can be customized to enhance functionality further.

## Features
- Extracts and processes questions from an input file.
- Generates detailed, structured answers for each question.
- Supports customization of prompt templates for different use cases.
- Includes dummy input and output files for reference.

## Setup Instructions

### Prerequisites
- Python installed on your system.
- OpenAI API key.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/tw-vaibhavwaykole/agent-extract-exam-solutions.git
   cd agent-extract-exam-solutions
   ```

2. **Install Dependencies**:
   Install the required Python libraries using:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OpenAI API Key**:
   - Copy the template file to create your `.env`:
     ```bash
     cp .env.template .env
     ```
   - Update the `.env` file with your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

   > Note: Any changes to your local `.env` file will be ignored by Git, keeping your API key safe.

4. **Run the Script**:
   - Provide the input file path in the script.
   - Run the main script to generate answers:
     ```bash
     python main.py
     ```

5. **View Outputs**:
   - Generated answers will be saved in the specified output file.
   - Refer to the dummy output file (`dummy_output.txt`) for the expected format.

## Files and References

- **Input File**:
  Contains the list of questions to be processed. Update the file path in the script to use your custom input file.

- **Dummy Output File**:
  Provides a reference for the format and structure of the generated answers.

- **Prompt Template**:
  The default prompt template is optimized for LLM exam questions but can be modified to suit different requirements.

## Enhancements
- The prompt template can be tailored to other domains or types of exams.
- Support for additional input and output formats (e.g., CSV, JSON).
- Integration with other APIs or tools for enhanced functionality. 

## Notes
- Ensure that the `.env` file is properly configured with your OpenAI API key before running the script.
- Sensitive keys should not be committed to the repository. Use `.gitignore` to exclude the `.env` file.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

Feel free to contribute or raise issues to enhance this project further!
