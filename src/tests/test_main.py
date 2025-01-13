import unittest
import sys
import os

# Add the parent directory to system path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import *  # Import your main functions here

class TestAIAgent(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def tearDown(self):
        """Clean up after each test method."""
        pass

    def test_basic_functionality(self):
        """Test basic functionality of the AI agent."""
        # Add your test cases here
        self.assertTrue(True)  # Placeholder test

    def test_data_loading(self):
        """Test if data is loaded correctly."""
        input_file = 'data/input/all-question-papers.txt'
        self.assertTrue(os.path.exists(input_file))

if __name__ == '__main__':
    unittest.main() 