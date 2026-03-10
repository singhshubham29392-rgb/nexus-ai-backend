import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv(GEMINI_API_KEY))

class TaskAgent:

    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def analyze_requirement(self, user_input: str):

        try:

            prompt = f"""
You are Nexus AI assistant.

User message:
{user_input}

Rules:
- If greeting → reply normally
- If project request → give structured plan
"""

            response = self.model.generate_content(prompt)

            return response.text

        except Exception as e:
            return f"AI Error: {str(e)}"


nexus_agent = TaskAgent()
