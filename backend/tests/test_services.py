import asyncio
import unittest
from unittest.mock import MagicMock, patch
from services.chat_engine import chat_engine, ChatEngine
from services.form_parser import GoogleFormParser

class TestServices(unittest.IsolatedAsyncioTestCase):
    
    async def test_chat_engine_flow(self):
        """Test the logic of determining the next question"""
        print("\nTesting Chat Engine Logic...")
        
        # logical schema
        schema = {
            "questions": [
                {
                    "id": "q1",
                    "title": "What's your name?",
                    "type": "short_text",
                    "required": True
                },
                {
                    "id": "q2",
                    "title": "Choose a color",
                    "type": "multiple_choice",
                    "options": ["Red", "Blue"],
                    "required": True
                }
            ]
        }
        
        # 1. Start - No history
        q1 = chat_engine.get_next_question(schema, [])
        self.assertIsNotNone(q1)
        self.assertEqual(q1["id"], "q1")
        self.assertEqual(q1["text"], "What's your name?")
        print("[OK] First question retrieved correctly")
        
        # 2. Answered first
        history = [{"question_id": "q1", "answer": "Alice"}]
        q2 = chat_engine.get_next_question(schema, history)
        self.assertIsNotNone(q2)
        self.assertEqual(q2["id"], "q2")
        self.assertEqual(q2["type"], "multiple_choice")
        print("[OK] Second question retrieved correctly")
        
        # 3. Answered all
        history.append({"question_id": "q2", "answer": "Red"})
        q3 = chat_engine.get_next_question(schema, history)
        self.assertIsNone(q3)
        print("[OK] Conversation completion detected")

    async def test_form_parser_extraction(self):
        """Test extracting questions from raw mock data"""
        print("\nTesting Form Parser Extraction...")
        parser = GoogleFormParser()
        
        # Mocking the raw data structure that comes from Google
        # This is a simplified version of the complex array structure
        mock_raw_data = [
            None,
            [
                None,
                [
                    # Question 1: Text
                    [
                        333, # Entry ID internal reference?
                        "What is your email?",
                        None,
                        0, # Short text ID
                        [[444, None, 0]] # Entry ID is here usually [444, null, 0]
                    ],
                    # Question 2: Choice
                    [
                        555,
                        "Preferred contact?",
                        None,
                        2, # Multiple Choice
                        [
                            [666, [["Email", None, None, None], ["Phone", None, None, None]], 1]
                        ]
                    ]
                ],
                None, None, None, None, None, None,
                "Test Form Title" # Form Title at [1][8]
            ]
        ]
        
        # We need to pacth the _extract_questions method logic or test the private method if we want
        # But let's test the public parse_form with patched fetch and parse_public_data
        
        with patch.object(parser, 'fetch_form_html', return_value="<html>...</html>"):
            with patch.object(parser, 'parse_public_data', return_value=mock_raw_data):
                result = await parser.parse_form("http://fake.url")
                
                self.assertEqual(result["title"], "Test Form Title")
                self.assertEqual(len(result["questions"]), 2)
                
                q1 = result["questions"][0]
                self.assertEqual(q1["title"], "What is your email?")
                self.assertEqual(q1["type"], "short_text")
                
                q2 = result["questions"][1]
                self.assertEqual(q2["title"], "Preferred contact?")
                self.assertEqual(q2["type"], "multiple_choice")
                self.assertEqual(q2["options"], ["Email", "Phone"])
                
                print("[OK] Form parsing logic confirmed")

if __name__ == "__main__":
    unittest.main()
