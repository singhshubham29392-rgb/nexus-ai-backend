import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class TaskAgent:

    def __init__(self):

        self.model = genai.GenerativeModel(
            "gemini-1.5-flash"
        )

    async def analyze_requirement(self, user_input: str):

        try:

            prompt = f"""
You are Nexus AI, a helpful AI assistant.

User message:
{user_input}

Rules:
- If the user greets → reply conversationally
- If user asks about project → give structured plan

For project requests include:
1. Title
2. Technical roadmap
3. Challenges
"""

            response = self.model.generate_content(prompt)

            return response.text

        except Exception as e:
            return f"AI Error: {str(e)}"


# Singleton instance
nexus_agent = TaskAgent()
