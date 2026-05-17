import os

class TestReportAnalyzer:
    def __init__(self, model_client):
        """
        Inject any model implementation (OpenAI, Gemini, etc.) 
        that has a 'generate_summary' method.
        """
        self.model_client = model_client

    def load_report(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Execution report not found at: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def load_executive_prompt(self, file_path="config/config_executive_report_prompt.txt"):
        """Reads the external system prompt from the configuration directory."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing prompt configuration file at: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def run_analysis(self, report_path: str):
        try:
            report_data = self.load_report(report_path)
        except Exception as e:
            return f"Error loading file: {e}"

        # Construct a strong, contextual system instruction for the AI
        system_instruction = self.load_executive_prompt()

        print(f"🤖 Sending data to {self.model_client.__class__.__name__}...")
        return self.model_client.generate_summary(system_instruction, report_data)