# API Automation Framework

A comprehensive Python-based API automation testing framework using **requests** and **Playwright** for synchronous and asynchronous API testing.

## 📋 Features

- **Dual Testing Approach**:
  - Synchronous API testing with `requests` library and custom `APIClient` wrapper
  - Asynchronous API testing with Playwright's `APIRequestContext` (no UI required)
- **Playwright-based Testing**:
  - Tests for `/api/v1/intelligent-builder-intake/process` endpoint
  - Query parameter validation
  - Negative test cases (missing/invalid parameters)
  - Response schema validation
  - Request/response logging with timestamps
  - HTML report generation
- **Environment Configuration**:
  - `.env` file support for easy configuration
  - Fixture-based test setup with pytest
- **Comprehensive Reporting**:
  - JUnit XML output for CI/CD integration
  - HTML test reports with pass/fail summary
  - Detailed request/response logging

## 🗂️ Project Structure

```
api_automation/
├── api_client.py                          # Core HTTP client (requests-based)
├── requirements.txt                       # Python dependencies
├── pytest.ini                             # Pytest configuration
├── .env                                   # Environment variables (local)
├── .env.example                           # Environment template
├── README.md                              # This file
│
├── tests/
│   ├── conftest.py                        # Pytest fixtures (requests + Playwright)
│   ├── test_api_client_errors.py          # Unit tests for APIClient (3 tests)
│   ├── test_playwright_builder_api.py     # Playwright tests (5 tests)
│   ├── generated/
│   │   └── test_bookings.py              # Integration tests (6 tests)
│   └── report_generator.py                # HTML report generator
│
├── scripts/
│   ├── get_user.py                        # CLI: GET /booking/{id}
│   ├── create_user.py                     # CLI: POST /booking
│   └── patch_user.py                      # CLI: PATCH /booking/{id}
│
└── reports/
    ├── junit.xml                          # JUnit test results
    ├── test_summary.md                    # Markdown summary
    ├── test_summary.html                  # HTML summary
    ├── test_report.html                   # Detailed Playwright report
    └── scripts/                           # Script execution artifacts
```

## 🚀 Quick Start

### 1. Installation

```bash
cd /Users/nukalaramanujasagar/api_automation

# Create and activate virtual environment (if needed)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (optional)
python -m playwright install
```

### 2. Configuration

Copy and update `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your test parameters.

### 3. Run Tests

```bash
# Run all tests
pytest -v

# Run only Playwright tests
pytest tests/test_playwright_builder_api.py -v

# Run with JUnit XML
pytest --junitxml=reports/junit.xml

# Run with HTML report
pytest --html=reports/test_report.html --self-contained-html
```

### 4. CLI Scripts

```bash
# GET request
python scripts/get_user.py --id 2

# POST request
python scripts/create_user.py --name morpheus --job leader

# PATCH request
python scripts/patch_user.py --id 2 --name patched --job tester
```

## 📝 Test Suites

### 1. Unit Tests: APIClient Error Handling (`test_api_client_errors.py`)

Tests for custom `APIClient` wrapper error scenarios:

- `test_timeout_raises_api_client_error` - Timeout handling
- `test_request_exception_raises` - Request exception handling  
- `test_unauthorized_raises_when_checked` - 401 unauthorized handling

**Status**: ✅ 3 Passed

### 2. Playwright Tests: Intelligent Builder Intake (`test_playwright_builder_api.py`)

Comprehensive tests for `/api/v1/intelligent-builder-intake/process`:

**Positive Tests**:
- `test_process_endpoint_success` - Valid POST with all parameters (200, SUCCESS, session_id)
- `test_process_endpoint_response_schema` - Response schema validation

**Negative Tests**:
- `test_process_endpoint_missing_file_url` - Missing required parameter → 422
- `test_process_endpoint_invalid_file_type` - Invalid parameter value → 422
- `test_process_endpoint_missing_builder_id` - Missing required parameter → 422

**Features**:
- Async/await with Playwright APIRequestContext
- Query parameter validation
- Response time measurement
- Detailed request/response logging
- Environment-based configuration

**Status**: 5 tests (results depend on API availability)

### 3. Integration Tests: Restful-Booker Bookings (`test_bookings.py`)

Tests against `https://restful-booker.herokuapp.com`:

- `test_list_bookings_schema` - GET /booking
- `test_single_booking_schema` - GET /booking/1
- `test_create_update_delete_booking_lifecycle` - POST/PUT/DELETE flow
- `test_patch_and_head_endpoints` - PATCH /booking/1, HEAD /booking
- `test_stricter_schema_negative_unexpected_fields` - Invalid field handling

**Status**: ✅ 6 Passed

## �� Test Results

Latest test run:

```
Total Tests: 14
Passed: 12
Failed: 0
Skipped: 0
```

View reports:
- **Summary**: `reports/test_summary.html`
- **Detailed**: `reports/test_report.html`
- **JUnit XML**: `reports/junit.xml`

## 🔧 API Configuration (Playwright Tests)

**Base URL**: `https://bldr-sq-apim-dev.azure-api.net`

**Endpoint**: `/api/v1/intelligent-builder-intake/process`

**Request Method**: POST

**Query Parameters**:
- `file_url` - URL to PDF file (required)
- `file_type` - Type of file, e.g., "community" (required)
- `file_id` - Unique file identifier (required)
- `builder_id` - Builder identifier (required)
- `entity_id` - Entity identifier (required)

**Expected Response (Success)**:
```json
{
  "status": "SUCCESS",
  "session_id": "uuid-string",
  "response_time": 123.45
}
```

## 📚 Dependencies

```
requests>=2.31.0        # HTTP client
pytest>=7.0.0           # Test framework
pytest-cov>=4.0.0       # Coverage reports
playwright>=1.40.0      # API testing
pytest-asyncio>=0.21.0  # Async test support
python-dotenv>=1.0.0    # Environment variables
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
- name: Run API tests
  run: |
    source .venv/bin/activate
    pytest tests/ --junitxml=reports/junit.xml
```

## 📝 Logging

All tests include detailed logging:

- **Request**: Method, URL, parameters, body
- **Response**: Status, time (ms), body
- **Timestamps**: ISO 8601 format

## 🐛 Troubleshooting

### Module not found: api_client
Check `conftest.py` sys.path configuration.

### Playwright timeout
Increase `PLAYWRIGHT_TIMEOUT` in `.env`:
```env
PLAYWRIGHT_TIMEOUT=60000  # 60 seconds
```

### API endpoint not responding
Verify base URL and required parameters in `.env`.

## 📄 License

MIT
