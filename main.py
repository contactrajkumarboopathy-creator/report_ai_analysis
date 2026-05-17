# Version 2.1.1  updated from local machine on 2024-06-15

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure the project root is on sys.path so src imports resolve when running main.py directly
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.analyzer import TestReportAnalyzer
#from src.models.openai_impl import OpenAIClient
from src.models.gemini_impl import GeminiClient

# Load the environment keys from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    # 1. Path to your log file
    report_path = "reports/web_regression_report.txt"
    
    # Quick guard to generate dummy data if you don't have a report yet
    if not os.path.exists(report_path):
        os.makedirs("reports", exist_ok=True)
        with open(report_path, "w") as f:
            f.write("FAIL: test_login_validation\nError: Timeout waiting for element '#dashboard'\n"
                    "FAIL: test_checkout_api\nError: 500 Internal Server Error at /api/v1/pay")

    # 2. Pick your engine (Swap GeminiClient() for OpenAIClient() whenever you want)
    # selected_model = OpenAIClient()
    selected_model = GeminiClient() 
    
    # 3. Initialize engine and run
    analyzer = TestReportAnalyzer(model_client=selected_model)
    analysis_result = analyzer.run_analysis(report_path)
    
    print("\n=================== ANALYSIS REPORT ===================")
    print(analysis_result)
    print("=======================================================")

if __name__ == "__main__":
    main()