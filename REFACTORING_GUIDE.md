# Dynamic Payload Framework - Refactoring Guide

## Overview

The API automation framework has been refactored to **avoid hardcoding** and support **multiple files dynamically** through pytest parameterization.

## Key Changes

### 1. **Removed Hardcoding from .env**

**Before:**
```env
BASE_URL=https://bldr-sq-apim-dev.azure-api.net
API_ENDPOINT=/api/v1/intelligent-builder-intake/process
PDF_FILE_URL=https://example.com/arbor-ridge-sitemap.pdf  # HARDCODED
FILE_TYPE=community                                        # HARDCODED
FILE_ID=arbor_ridge_001                                   # HARDCODED
BUILDER_ID=smith_douglas                                  # HARDCODED
ENTITY_ID=arbor_ridge                                     # HARDCODED
PLAYWRIGHT_TIMEOUT=30000
PLAYWRIGHT_RETRIES=3
```

**After:**
```env
BASE_URL=https://bldr-sq-apim-dev.azure-api.net
API_ENDPOINT=/api/v1/intelligent-builder-intake/process
PLAYWRIGHT_TIMEOUT=30000
PLAYWRIGHT_RETRIES=3
```

✅ File data is now managed externally in `tests/test_data.py`

### 2. **Test Data Management** - `tests/test_data.py`

Centralized test data with 5 predefined combinations:

```python
TEST_CASES = [
    {
        "file_url": "https://example.com/community-guide.pdf",
        "file_type": "community",
        "file_id": "community_001",
        "builder_id": "builder_alpha",
        "entity_id": "entity_alpha",
        "description": "Community guide PDF for Builder Alpha",
    },
    # ... more test cases
]
```

**Benefits:**
- All test data in one place
- Easy to add new file combinations
- Reusable across multiple tests
- Clear descriptions for each test case

### 3. **Payload Builder** - `tests/payload_builder.py`

Dynamic payload construction without hardcoding:

```python
# Build from test data
payload = PayloadBuilder.build_query_params("community_001")

# Build custom payload
payload = PayloadBuilder.build_query_params_custom(
    file_url="https://...",
    file_type="community",
    file_id="custom_001",
    builder_id="my_builder",
    entity_id="my_entity",
)
```

### 4. **Parameterized Tests** - `tests/test_dynamic_payload.py`

Tests now run with **all test data combinations** automatically:

```python
@pytest.mark.parametrize("test_case", get_all_test_cases(), ids=get_test_case_ids())
async def test_process_endpoint_success_parametrized(self, api_config, test_logger, test_case):
    # Builds payload dynamically from test_case
    payload = PayloadBuilder.build_query_params(test_case["file_id"])
    # ... test logic
```

**Test execution:**
```
test_process_endpoint_success_parametrized[community_001] PASSED
test_process_endpoint_success_parametrized[zoning_001] PASSED
test_process_endpoint_success_parametrized[image_001] PASSED
test_process_endpoint_success_parametrized[blueprint_001] PASSED
test_process_endpoint_success_parametrized[brochure_001] PASSED
```

## Test Data Structure

Each test case contains:

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `file_url` | string | `https://example.com/guide.pdf` | URL to process |
| `file_type` | string | `community`, `zoning`, `image` | File classification |
| `file_id` | string | `community_001` | Unique identifier |
| `builder_id` | string | `builder_alpha` | Builder context |
| `entity_id` | string | `entity_alpha` | Entity context |
| `description` | string | `Community guide for Builder A` | Human-readable label |

## Supported File Types

Based on API validation:

```
lookbook, blueprint, specsheet, community, brochure, marked up plan, other,
thumbnail, frame preview, delivery image, invoice, project manual, purchase
order, part list, unmapped part list, window schedule, roof truss layout,
floor truss layout, wall panel layout, engineered layout, plat map, zoning,
hoa, community brochure, community specsheet, video, post image, image, logo,
favicon
```

## Running Tests

### Run all parameterized tests:
```bash
pytest tests/test_dynamic_payload.py -v
```

### Run specific test combination:
```bash
pytest tests/test_dynamic_payload.py::TestIntelligentBuilderIntake::test_process_endpoint_success_parametrized[community_001] -v
```

### Run all tests with output capture:
```bash
pytest tests/test_dynamic_payload.py -v -s
```

### Run only parametrized success tests:
```bash
pytest tests/test_dynamic_payload.py::TestIntelligentBuilderIntake -v
```

## Adding New Test Cases

1. Open `tests/test_data.py`
2. Add to `TEST_CASES` list:

```python
{
    "file_url": "https://example.com/new-document.pdf",
    "file_type": "specsheet",
    "file_id": "specsheet_001",
    "builder_id": "builder_zeta",
    "entity_id": "entity_zeta",
    "description": "Spec sheet for Builder Zeta",
},
```

3. Tests automatically run for the new combination

## Request Logging Example

For each test case, logs include:

```
[INFO] 🔄 Processing file: Community guide PDF for Builder Alpha
[INFO] REQUEST: POST /api/v1/intelligent-builder-intake/process
[INFO]   Query Params: {
  "file_url": "https://example.com/community-guide.pdf",
  "file_type": "community",
  "file_id": "community_001",
  "builder_id": "builder_alpha",
  "entity_id": "entity_alpha"
}
[INFO] RESPONSE: Status 200
[INFO]   Response Time: 1339.86ms
[INFO]   Data: { ... response payload ... }
```

## Validation

Each test validates:

✅ HTTP status code (200 or 202)
✅ Response contains required fields (`status: SUCCESS`)
✅ File-specific payload is logged
✅ Response time is tracked

## Negative Tests

Included tests for error handling:

```python
test_invalid_file_type()      # Expects 422 for invalid file_type
test_missing_required_parameter()  # Expects 422 for missing file_url
```

## Architecture Benefits

1. **No Hardcoding**: All test data is external
2. **Scalability**: Add 100+ test combinations easily
3. **Maintainability**: Change data without touching test code
4. **Reusability**: PayloadBuilder works for any test scenario
5. **Visibility**: Clear logging for each file processed
6. **Parallel Ready**: Parametrization supports parallel execution

## File Organization

```
tests/
├── test_data.py              # Test case definitions (5+ combinations)
├── payload_builder.py        # Payload construction logic
├── test_dynamic_payload.py   # Parametrized tests (12 test functions)
├── test_community_api.py     # Legacy tests (can be removed)
├── conftest.py              # Fixtures (updated to remove hardcoding)
└── ...
```

## Migration Path

If using old hardcoded tests (`test_community_api.py`):

1. ✅ Keep for backward compatibility
2. ✅ Migrate assertions to `test_dynamic_payload.py`
3. ✅ Update `.env` to only store base config
4. ✅ Add new test cases to `test_data.py`
5. ✅ Run all tests together: `pytest tests/ -v`

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| Test Data | Hardcoded in `.env` | External `test_data.py` |
| Test Cases | Single combination | 5+ parameterized combinations |
| Payload Building | Manual strings | `PayloadBuilder` class |
| Logging | Generic | File-specific, detailed |
| Scalability | Limited | Unlimited combinations |
| Maintenance | High | Low |
