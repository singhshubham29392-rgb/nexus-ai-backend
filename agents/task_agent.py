import google.generativeai as genai
from app.core.config import settings
from app.core.constants import AIConfig


class TaskAgent:

    def __init__(self):
        # Initialize Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)

        self.model = genai.GenerativeModel(
            settings.GEMINI_MODEL_NAME
        )

    async def analyze_requirement(self, user_input: str) -> str:
        """
        Processes user input and returns either a conversational reply
        or a structured project roadmap.
        """

        try:

            prompt = f"""
You are Nexus AI, a helpful AI assistant.

User message:
{user_input}

Rules:
- If the user greets or chats → respond conversationally.
- If the user asks about a project/task → provide a structured plan.

For project requests include:
1. Title
2. 3-step technical roadmap
3. Priority level
"""

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=AIConfig.MAX_OUTPUT_TOKENS,
                    temperature=AIConfig.TEMPERATURE,
                )
            )

            # Safe response handling
            if response and response.text:
                return response.text
            else:
                return "Nexus AI couldn't generate a response."

        except Exception as e:
            return f"Nexus Agent Error: {str(e)}"


# Singleton instance
nexus_agent = TaskAgent()