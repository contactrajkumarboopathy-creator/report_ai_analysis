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

    def run_analysis(self, report_path: str):
        try:
            report_data = self.load_report(report_path)
        except Exception as e:
            return f"Error loading file: {e}"

        # Construct a strong, contextual system instruction for the AI
        system_instruction = (
            "You are a Principal QA Automation Architect. Analyze the provided test report. "
            "Provide a summary with: 1) Execution Coverage Overview, "
            "2) Error Root Cause Analysis, and 3) Actionable Code/Infrastructure Resolutions."
        )

        print(f"🤖 Sending data to {self.model_client.__class__.__name__}...")
        return self.model_client.generate_summary(system_instruction, report_data)