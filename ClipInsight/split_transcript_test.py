import unittest
from llm_model import split_transcript

class TestClass(unittest.TestCase):
    # empty transcript provided
    def test_with_empty_transcript(self):
        result = split_transcript("")
        expected_output = []
        self.assertEqual(expected_output, result)
    
    # transcript provided
    def test_with_transcript(self):
        transcript = "This is a large piece of text that needs to be split into chunks. It should be split based on the number of characters in each chunk."
        result = split_transcript(transcript)
        expected_result = ['This is a large piece of text that needs to be split into chunks. It should ''be split based on the number of characters in each chunk.']
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()