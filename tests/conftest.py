"""Pytest configuration and fixtures for Playwright-based API testing.

Supports:
- Playwright async API testing with APIRequestContext
- Intelligent Builder Intake API endpoints
"""
import sys
import os
import pytest
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Ensure project root is on sys.path so imports like `api_client` resolve during tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from test_data import TEST_CASES


# ============= Playwright-based fixtures =============

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop


@pytest.fixture
def api_config():
    """Load API configuration from environment with test data.
    
    Combines API endpoint configuration with the first test case from test_data.py
    """
    # Get the first test case as default
    test_case = TEST_CASES[0]
    
    return {
        "base_url": os.getenv("BASE_URL", "https://bldr-sq-apim-dev.azure-api.net"),
        "endpoint": os.getenv("API_ENDPOINT", "/api/v1/intelligent-builder-intake/process"),
        "timeout": int(os.getenv("PLAYWRIGHT_TIMEOUT", "60000")),
        "retries": int(os.getenv("PLAYWRIGHT_RETRIES", "3")),
        "file_url": test_case["file_url"],
        "file_type": test_case["file_type"],
        "file_id": test_case["file_id"],
        "builder_id": test_case["builder_id"],
        "entity_id": test_case["entity_id"],
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
