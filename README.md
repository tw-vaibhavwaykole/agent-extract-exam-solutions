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

   To generate a full list of installed dependencies (useful for debugging):
   ```bash
   pip freeze > requirements_full.txt
   ```

   Note: requirements_full.txt is git-ignored and should not be committed.

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

4. **Prepare Input File**:
   - Place your question paper in `data/input/all-question-papers.txt`
   - Or set custom input file name in `.env`:
     ```
     INPUT_FILE=your-questions.txt
     ```
   - If no input file exists, an example template will be created automatically

5. **Run the Script**:
   ```bash
   python main.py
   ```
   - Generated answers will be saved in `data/output/`

6. **View Outputs**:
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

## Testing

This project uses pytest for testing. Here are the different ways to run tests:

### 1. Basic Testing

Run all tests:
```bash
pytest src/tests/
```

Run a specific test file:
```bash
pytest src/tests/test_main.py
```

Run a specific test case:
```bash
pytest src/tests/test_main.py::TestAIAgent::test_basic_functionality
```

### 2. Testing with Coverage

Run tests with coverage report:
```bash
pytest --cov=src src/tests/
```

Generate HTML coverage report:
```bash
pytest --cov=src --cov-report=html src/tests/
```
The HTML report will be available in `htmlcov/index.html`

Generate XML coverage report (used by CI):
```bash
pytest --cov=src --cov-report=xml src/tests/
```

### 3. Verbose Testing

Run tests with detailed output:
```bash
pytest -v src/tests/
```

Show print statements during tests:
```bash
pytest -s src/tests/
```

### 4. Running Tests Locally with Environment Variables

```bash
# Set up environment variables
export OPENAI_API_KEY=your_api_key_here

# Run tests
pytest src/tests/
```

Or using a .env file:
```bash
# Create .env file if it doesn't exist
cp .env.template .env

# Edit .env with your API key
# Then run tests
pytest src/tests/
```

### 5. Development Testing

Watch for changes and run tests automatically:
```bash
pytest-watch src/tests/
```

### 6. Code Quality Checks

Run linting checks:
```bash
# Run flake8
flake8 src/

# Run black (code formatting)
black --check src/

# Run isort (import sorting)
isort --check-only src/
```

Fix formatting issues:
```bash
# Apply black formatting
black src/

# Fix import sorting
isort src/
```

### Test Structure

```
src/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── conftest.py (if needed for fixtures)
```

### Continuous Integration

Tests are automatically run on GitHub Actions:
- On every push to main branch
- On every pull request
- Using multiple Python versions (3.8, 3.9, 3.10)
- With code coverage reporting to Codecov

You can view the test results:
1. In the GitHub Actions tab
2. In the pull request checks
3. On Codecov for coverage reports

### Adding New Tests

1. Create test files in `src/tests/`
2. Name test files with `test_` prefix
3. Name test classes with `Test` prefix
4. Name test methods with `test_` prefix

Example:
```python
# src/tests/test_feature.py
import unittest

class TestNewFeature(unittest.TestCase):
    def test_specific_functionality(self):
        self.assertTrue(True)
```

## CI/CD

This project uses GitHub Actions for continuous integration and deployment. The following checks are performed on each push and pull request:

- Python tests on multiple Python versions (3.8, 3.9, 3.10)
- Code coverage reporting
- Code linting (flake8, black, isort)

Status badges:
![Tests](https://github.com/{username}/{repo-name}/workflows/Python%20Tests/badge.svg)
![Linting](https://github.com/{username}/{repo-name}/workflows/Linting/badge.svg)

## Code Formatting

Format and check your code:

```bash
# Format code
black .
isort .

# Check formatting
black --check .
isort --check-only .
flake8 .
```
