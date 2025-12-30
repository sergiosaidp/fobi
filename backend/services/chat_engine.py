from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class ChatEngine:
    def __init__(self):
        pass

    def get_next_question(self, schema: Dict, conversation_history: List[Dict]) -> Optional[Dict]:
        """
        Determine the next question based on the schema and history.
        This is a simple sequential engine for now.
        """
        questions = schema.get("questions", [])
        if not questions:
            return None

        # Count how many questions have been answered
        answered_count = len(conversation_history)
        
        # If we have answered all, we are done
        if answered_count >= len(questions):
            return None
            
        # Get the next question
        next_q = questions[answered_count]
        
        return {
            "id": next_q.get("id"),
            "text": next_q.get("title"),
            "type": next_q.get("type"),
            "options": next_q.get("options"),
            "required": next_q.get("required"),
            "placeholder": next_q.get("description") or "Type your answer..."
        }

    def validate_answer(self, question: Dict, answer: Any) -> bool:
        """
        Validate the answer format based on question type.
        """
        q_type = question.get("type", "short_text")
        
        # Simple validation logic
        if not answer and question.get("required"):
            return False
            
        if q_type == "multiple_choice" or q_type == "dropdown":
            if answer and answer not in question.get("options", []):
                return False # Answer must be one of the options
                
        return True

chat_engine = ChatEngine()
