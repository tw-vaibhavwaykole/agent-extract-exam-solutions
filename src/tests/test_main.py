import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add the parent directory to system path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAIAgent(unittest.TestCase):
    @patch('langchain_openai.OpenAI')
    def setUp(self, mock_openai):
        """Set up test fixtures before each test method."""
        # Mock OpenAI to prevent actual API calls during tests
        self.mock_openai = mock_openai
        self.mock_openai.return_value = Mock()

    def tearDown(self):
        """Clean up after each test method."""
        pass

    def test_basic_functionality(self):
        """Test basic functionality of the AI agent."""
        # Add your test cases here
        self.assertTrue(True)  # Placeholder test

    def test_data_loading(self):
        """Test if data is loaded correctly."""
        input_file = "data/input/all-question-papers.txt"
        self.assertTrue(os.path.exists(input_file))


if __name__ == "__main__":
    unittest.main()
