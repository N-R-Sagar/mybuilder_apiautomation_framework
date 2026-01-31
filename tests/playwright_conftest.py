"""Playwright API testing fixtures and configuration."""
import pytest
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def api_config():
    """Load API configuration from environment."""
    return {
        "base_url": os.getenv("BASE_URL", "https://bldr-sq-apim-dev.azure-api.net"),
        "endpoint": os.getenv("API_ENDPOINT", "/api/v1/intelligent-builder-intake/process"),
        "file_url": os.getenv("PDF_FILE_URL", "https://example.com/arbor-ridge-sitemap.pdf"),
        "file_type": os.getenv("FILE_TYPE", "community"),
        "file_id": os.getenv("FILE_ID", "arbor_ridge_001"),
        "builder_id": os.getenv("BUILDER_ID", "smith_douglas"),
        "entity_id": os.getenv("ENTITY_ID", "arbor_ridge"),
        "timeout": int(os.getenv("PLAYWRIGHT_TIMEOUT", "30000")),
        "retries": int(os.getenv("PLAYWRIGHT_RETRIES", "3")),
    }


@pytest.fixture
def test_logger():
    """Simple test logger for request/response details."""
    class TestLogger:
        def __init__(self):
            self.logs = []
            self.start_time = datetime.now()

        def log(self, message, level="INFO"):
            entry = {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message,
            }
            self.logs.append(entry)
            print(f"[{level}] {message}")

        def log_request(self, method, url, params=None, json_body=None):
            self.log(f"REQUEST: {method} {url}")
            if params:
                self.log(f"  Query Params: {json.dumps(params, indent=2)}")
            if json_body:
                self.log(f"  Body: {json.dumps(json_body, indent=2)}")

        def log_response(self, status, data=None, response_time_ms=None):
            self.log(f"RESPONSE: Status {status}")
            if response_time_ms:
                self.log(f"  Response Time: {response_time_ms}ms")
            if data:
                self.log(f"  Data: {json.dumps(data, indent=2)}")

        def get_report(self):
            """Generate a simple text report of all logs."""
            report = f"Test Execution Report\n"
            report += f"Start Time: {self.start_time}\n"
            report += f"End Time: {datetime.now()}\n"
            report += f"Total Logs: {len(self.logs)}\n\n"
            report += "Logs:\n"
            for log in self.logs:
                report += f"[{log['timestamp']}] [{log['level']}] {log['message']}\n"
            return report

    return TestLogger()
