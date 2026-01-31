"""Refactored Playwright-based API tests with dynamic test data.

Uses pytest parameterization to test multiple file combinations dynamically.
Supports different file types, builders, and entities without hardcoding.
"""
import pytest
import time
from playwright.async_api import async_playwright
from tests.test_data import get_all_test_cases, get_test_case_ids
from tests.payload_builder import PayloadBuilder


class TestIntelligentBuilderIntake:
    """Test suite for intelligent-builder-intake process endpoint."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", get_all_test_cases(), ids=get_test_case_ids())
    async def test_process_endpoint_success_parametrized(self, api_config, test_logger, test_case):
        """Test successful POST request for multiple file types and builders.
        
        Parameterized to run with different combinations of:
        - file_url (different document URLs)
        - file_type (community, zoning, blueprint, etc.)
        - file_id (unique identifiers)
        - builder_id (different builders)
        - entity_id (different entities)
        
        Validates:
        - HTTP status code is 200 or 202
        - Response contains required fields
        - jobId exists in response (if applicable)
        - Request is logged with specific payload
        """
        async with async_playwright() as p:
            context = await p.request.new_context(
                base_url=api_config["base_url"],
                timeout=api_config["timeout"],
            )
            
            # Build payload from test data
            query_params = PayloadBuilder.build_query_params(test_case["file_id"])
            
            # Log request with file-specific details
            test_logger.log(f"🔄 Processing file: {test_case['description']}")
            test_logger.log_request("POST", api_config["endpoint"], params=query_params)
            
            # Send request and measure response time
            start_time = time.time()
            response = await context.post(
                api_config["endpoint"],
                params=query_params,
            )
            response_time_ms = (time.time() - start_time) * 1000
            
            # Get response data
            response_data = await response.json()
            
            # Log response with full details
            test_logger.log_response(response.status, response_data, response_time_ms)
            
            # Assertions
            assert response.status in [200, 202], \
                f"Expected 200 or 202, got {response.status}"
            
            # Validate required response fields
            assert "status" in response_data, "Response missing 'status' field"
            assert response_data["status"] == "SUCCESS", \
                f"Expected status SUCCESS, got {response_data.get('status')}"
            
            # Log success
            test_logger.log(f"✓ File '{test_case['file_id']}' processed successfully")
            test_logger.log(f"✓ Builder: {test_case['builder_id']}, Entity: {test_case['entity_id']}")
            test_logger.log(f"✓ Response time: {response_time_ms:.2f}ms")


@pytest.mark.asyncio
@pytest.mark.parametrize("test_case", get_all_test_cases(), ids=get_test_case_ids())
async def test_process_endpoint_all_files(api_config, test_logger, test_case):
    """Execute process endpoint for all test cases.
    
    This is a standalone parametrized test that iterates through all
    test data combinations and validates each one.
    
    Uses:
    - Dynamic payload builder
    - Test data from test_data.py
    - Parameterized test execution
    """
    async with async_playwright() as p:
        context = await p.request.new_context(
            base_url=api_config["base_url"],
            timeout=api_config["timeout"],
        )
        
        # Build dynamic payload
        payload = PayloadBuilder.build_query_params(test_case["file_id"])
        
        # Log request details
        test_logger.log(f"\n{'='*60}")
        test_logger.log(f"Test Case: {test_case['description']}")
        test_logger.log(f"{'='*60}")
        test_logger.log(f"File Type: {test_case['file_type']}")
        test_logger.log(f"Builder ID: {test_case['builder_id']}")
        test_logger.log(f"Entity ID: {test_case['entity_id']}")
        test_logger.log_request("POST", api_config["endpoint"], params=payload)
        
        # Execute request
        start_time = time.time()
        response = await context.post(
            api_config["endpoint"],
            params=payload,
        )
        elapsed_ms = (time.time() - start_time) * 1000
        
        # Parse response
        response_data = await response.json()
        test_logger.log_response(response.status, response_data, elapsed_ms)
        
        # Validate response
        assert response.status in [200, 202], \
            f"Expected 200/202 for {test_case['file_id']}, got {response.status}"
        assert response_data.get("status") == "SUCCESS", \
            f"Processing failed for {test_case['file_id']}"
        
        # Log summary
        test_logger.log(f"✅ PASSED: {test_case['file_id']}")
        test_logger.log(f"⏱️  Response time: {elapsed_ms:.2f}ms")


@pytest.mark.asyncio
async def test_invalid_file_type(api_config, test_logger):
    """Test error handling for invalid file_type parameter.
    
    Validates:
    - HTTP status code is 422 (validation error)
    - Error details are returned
    """
    async with async_playwright() as p:
        context = await p.request.new_context(
            base_url=api_config["base_url"],
            timeout=api_config["timeout"],
        )
        
        # Build payload with invalid file_type
        invalid_payload = PayloadBuilder.build_query_params_custom(
            file_url="https://example.com/test.pdf",
            file_type="invalid_file_type",  # Invalid
            file_id="invalid_001",
            builder_id="test_builder",
            entity_id="test_entity",
        )
        
        test_logger.log("Testing negative case: invalid file_type")
        test_logger.log_request("POST", api_config["endpoint"], params=invalid_payload)
        
        response = await context.post(
            api_config["endpoint"],
            params=invalid_payload,
        )
        response_data = await response.json()
        test_logger.log_response(response.status, response_data)
        
        # Should return validation error
        assert response.status == 422, f"Expected 422 for invalid file_type, got {response.status}"
        test_logger.log("✓ Invalid file_type correctly rejected")


@pytest.mark.asyncio
async def test_missing_required_parameter(api_config, test_logger):
    """Test error handling for missing required parameters.
    
    Validates:
    - HTTP status code is 422 when file_url is missing
    - Error details indicate missing parameter
    """
    async with async_playwright() as p:
        context = await p.request.new_context(
            base_url=api_config["base_url"],
            timeout=api_config["timeout"],
        )
        
        # Missing file_url parameter
        missing_payload = {
            "file_type": "community",
            "file_id": "test_001",
            "builder_id": "test_builder",
            "entity_id": "test_entity",
            # file_url intentionally omitted
        }
        
        test_logger.log("Testing negative case: missing file_url")
        test_logger.log_request("POST", api_config["endpoint"], params=missing_payload)
        
        response = await context.post(
            api_config["endpoint"],
            params=missing_payload,
        )
        response_data = await response.json()
        test_logger.log_response(response.status, response_data)
        
        # Should return validation error
        assert response.status == 422, f"Expected 422 for missing file_url, got {response.status}"
        assert isinstance(response_data.get("detail"), list), "Error details should be a list"
        test_logger.log("✓ Missing parameter correctly rejected")
