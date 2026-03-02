import os
import base64
from openai import OpenAI

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('LLM_API_KEY'), base_url="https://api.deepseek.com")

    def check_transcription(self, user_transcription:str) -> str:
       
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                self._system_message(),
                {"role": "user", "content": user_transcription},
            ],
            stream=False
        )

        result = response.choices[0].message.content
        print("LLM Response:", result)
        return result

    def _system_message(self):
        return {
            "role": "system",
            "content": """You are an examiner assessing a Cambridge B2 First (FCE) Speaking Part 2 task (comparing two pictures).
Evaluate my response according to the following criteria. Be concise and give a score from 1–5 for each category, plus specific improvement advice.

Assess whether my answer: 
- Direct comparison (similarities and differences)
- Clear answer to the final question
- Focuses on comparison rather than separate description
- Uses comparative language (e.g., both, whereas, while, compared to, unlike)
- Avoids describing one picture fully before moving to the other
- Natural flow
- Uses appropriate speculation language: e.g., might, could, may, seem to, perhaps, probably
- Uses a range of linking words: e.g., however, on the other hand, similarly, whereas
- Shows grammatical range and accuracy
- Modals
- No repeated serious errors
- Demonstrates clear pronunciation (if transcript suggests issues)
- Natural phrasing
- No unnatural repetition
- Uses varied and appropriate vocabulary
- Avoids basic repetition (e.g., good, nice, thing, people)
- Sounds natural in English
- Natural collocations
"""
        }