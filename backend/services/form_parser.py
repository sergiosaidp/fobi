import aiohttp
from bs4 import BeautifulSoup
import re
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class GoogleFormParser:
    def __init__(self):
        self.session = None

    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def fetch_form_html(self, url: str) -> str:
        """Fetch the HTML content of the Google Form"""
        session = await self.get_session()
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch form: {response.status}")
            return await response.text()

    def parse_public_data(self, html: str) -> Dict[str, Any]:
        """
        Extract the FB_PUBLIC_LOAD_DATA from the HTML.
        This contains the raw form definition in a JSON-like structure.
        """
        match = re.search(r'var FB_PUBLIC_LOAD_DATA_ = (.*?);', html)
        if not match:
            raise Exception("Could not find form data in page")
        
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            raise Exception("Failed to parse form data JSON")

    def _extract_questions(self, raw_data: List) -> List[Dict]:
        """
        Extract question details from the raw Google Form data structure.
        Structure analysis based on common Google Form patterns:
        [1][1] contains the list of form items
        Each item:
        - [1]: Question Title
        - [2]: Question Description (can be None or empty)
        - [3]: Question Type ID (0: Short Answer, 1: Paragraph, 2: Multiple Choice, 3: Dropdown, 4: Checkboxes)
        - [4]: Options list (for Choice/Dropdown/Checkboxes)
           - [0][1]: Config info including possible answers
        - [4][0][0]: Entry ID (needed for submission)
        """
        questions = []
        
        try:
            # The form items are usually at index 1, index 1 of the main array
            form_items = raw_data[1][1]
            
            if not form_items:
                return []

            for item in form_items:
                # Basic validation request to ensure it is a valid item structure
                if not item or len(item) < 2:
                    continue

                # Skip non-question items (like section headers which have different IDs)
                # Usually questions have a specific ID structure at item[3]
                
                question_title = item[1]
                question_desc = item[2] if len(item) > 2 else ""
                question_type_id = item[3]
                
                # Default unknown
                question_type = "unknown"
                options = []
                entry_id = None
                required = False

                # Extract Entry ID and Required status
                # Entry ID is often deep in the structure: item[4][0][0]
                if len(item) > 4 and item[4] and len(item[4]) > 0 and len(item[4][0]) > 0:
                    entry_id = item[4][0][0]
                    # Required status is often at item[4][0][2] (1 = required, 0 = not)
                    if len(item[4][0]) > 2:
                        required = bool(item[4][0][2])
                
                # Map Types
                if question_type_id == 0:
                    question_type = "short_text"
                elif question_type_id == 1:
                    question_type = "long_text"
                elif question_type_id == 2:
                    question_type = "multiple_choice"
                elif question_type_id == 3:
                    question_type = "dropdown"
                elif question_type_id == 4:
                    question_type = "checkboxes"
                
                # Extract Options for choice-based questions
                # Options are usually at item[4][0][1] which is a list of [value, null, null, null]
                if question_type in ["multiple_choice", "dropdown", "checkboxes"]:
                    if len(item) > 4 and item[4] and len(item[4]) > 0 and len(item[4][0]) > 1:
                        raw_options = item[4][0][1]
                        if raw_options:
                            options = [opt[0] for opt in raw_options if opt and len(opt) > 0]

                if entry_id: # Only add if we successfully found an entry ID, otherwise it's likely not a submittable question
                    questions.append({
                        "id": str(entry_id),
                        "title": question_title,
                        "description": question_desc,
                        "type": question_type,
                        "options": options,
                        "required": required
                    })
                    
        except Exception as e:
            logger.error(f"Error parsing specific question items: {str(e)}")
            # Continue with what we have or re-raise depending on strictness
            pass
            
        return questions

    async def parse_form(self, url: str) -> Dict[str, Any]:
        """Main entry point to parse a Google Form"""
        try:
            html = await self.fetch_form_html(url)
            
            # Using BeautifulSoup just for title/desc if needed, or fallback
            soup = BeautifulSoup(html, 'html.parser')
            form_title = soup.title.string if soup.title else "Untitled Form"
            
            # Extract raw data
            raw_data = self.parse_public_data(html)
            
            # Extract basic info from raw data if possible, usually at [1][8] or [1][0]
            # [1][8] is form title, [1][0] is description
            if len(raw_data) > 1:
                 if len(raw_data[1]) > 8:
                     form_title = raw_data[1][8] or form_title
            
            questions = self._extract_questions(raw_data)
            
            return {
                "title": form_title,
                "questions": questions,
                "raw_data_version": "1.0"
            }
            
        except Exception as e:
            logger.error(f"Failed to parse Google Form: {str(e)}")
            raise e

# specific instance to be used
form_parser = GoogleFormParser()
