from google import genai

class GeminiClient:
    def __init__(self):
        self.client = genai.Client() # Automatically reads GEMINI_API_KEY from environment

    def generate_summary(self, system_instruction: str, report_data: str) -> str:
        # We combine system instructions and payload for Gemini's simple layout
        full_prompt = f"{system_instruction}\n\nHere is the report data to analyze:\n\n{report_data}"
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
        )
        return response.text