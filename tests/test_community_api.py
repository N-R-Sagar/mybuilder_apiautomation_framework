"""Playwright-based API tests for intelligent-builder-intake process endpoint.

Tests the POST /api/v1/intelligent-builder-intake/process endpoint using Playwright's
APIRequestContext for non-UI API automation.
"""
import pytest
import json
import time
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_process_endpoint_success(api_config, test_logger):
    """Test successful POST request to process endpoint with valid parameters.
    
    Validates:
    - HTTP status code is 200
    - status = SUCCESS
    - response contains message field
    - response_time_ms > 0
    """
    async with async_playwright() as p:
        context = await p.request.new_context(
            base_url=api_config["base_url"],
            timeout=90000,  # 90 seconds to allow for document processing
        )
        # Prepare query parameters
        query_params = {
            "file_url": api_config["file_url"],
            "file_type": api_config["file_type"],
            "file_id": api_config["file_id"],
            "builder_id": api_config["builder_id"],
            "entity_id": api_config["entity_id"],
        }
        
        # Log request
        test_logger.log_request("POST", api_config["endpoint"], params=query_params)
        
        # Send request and measure response time
        start_time = time.time()
        response = await context.post(
            api_config["endpoint"],
            params=query_params,
            data=json.dumps({}),
            headers={"Content-Type": "application/json"},
        )
        response_time_ms = (time.time() - start_time) * 1000
        
        # Get response data
        response_data = await response.json()
        
        # Log response
        test_logger.log_response(response.status, response_data, response_time_ms)
        
        # Assertions
        assert response.status == 200, f"Expected 200, got {response.status}"
        assert response_data.get("status") == "SUCCESS", f"Expected status SUCCESS, got {response_data.get('status')}"
        assert response_data.get("message") is not None, "message field should not be null"
        assert response_time_ms > 0, "response_time should be positive"
        
        # Log success
        test_logger.log(f"✓ Process endpoint returned 200 with SUCCESS status")
        test_logger.log(f"✓ Message: {response_data.get('message')}")
        test_logger.log(f"✓ Response time: {response_time_ms:.2f}ms")


@pytest.mark.asyncio
async def test_process_endpoint_response_schema(api_config, test_logger):
    """Test response schema validation for successful requests.
    
    Validates:
    - Response contains required fields (status, message, response)
    - Field types are correct
    - No unexpected null values in critical fields
    """
    async with async_playwright() as p:
        context = await p.request.new_context(
            base_url=api_config["base_url"],
            timeout=90000,  # 90 seconds to allow for document processing
        )
        query_params = {
            "file_url": api_config["file_url"],
            "file_type": api_config["file_type"],
            "file_id": api_config["file_id"],
            "builder_id": api_config["builder_id"],
            "entity_id": api_config["entity_id"],
        }
        
        test_logger.log("Testing response schema validation")
        response = await context.post(
            api_config["endpoint"],
            params=query_params,
            data=json.dumps({}),
            headers={"Content-Type": "application/json"},
        )
        
        if response.status == 200:
            response_data = await response.json()
            
            # Display response body
            print("\n" + "="*80)
            print("RESPONSE BODY:")
            print("="*80)
            print(json.dumps(response_data, indent=2))
            print("="*80 + "\n")
            
            test_logger.log_response(response.status, response_data)
            
            # Validate required fields for success response
            required_fields = ["status", "message", "response"]
            for field in required_fields:
                assert field in response_data, f"Missing required field: {field}"
                # status and message should not be null
                if field in ["status", "message"]:
                    assert response_data[field] is not None, f"Field '{field}' should not be null"
            
            test_logger.log("✓ Response schema is valid")
            test_logger.log(f"✓ All required fields present: {required_fields}")
            test_logger.log(f"✓ Response includes document processing metadata")
            
            # Dataset Validation: Validate extracted community data
            print("\n" + "="*80)
            print("DATASET VALIDATION:")
            print("="*80)
            
            response_obj = response_data.get("response", {})
            document_metadata = response_obj.get("document_metadata", {})
            additional_metadata = document_metadata.get("additional_metadata", {})
            derived_fields = additional_metadata.get("derived_fields", {})
            
            # Validate document metadata structure
            assert "file_type" in response_obj, "Missing file_type in response"
            assert response_obj["file_type"] == "community", f"Expected file_type 'community', got '{response_obj['file_type']}'"
            
            # Validate document_metadata fields
            required_doc_fields = ["file_name", "file_type", "parsed_at", "parser", "page_count"]
            for field in required_doc_fields:
                assert field in document_metadata, f"Missing document_metadata field: {field}"
                assert document_metadata[field] is not None, f"Document metadata field '{field}' should not be null"
            
            # Validate parser type
            parser = document_metadata.get("parser", "")
            assert parser in ["azure_document_intelligence", "openai"], f"Invalid parser: {parser}"
            test_logger.log(f"✓ Parser validated: {parser}")
            
            # Validate page count
            page_count = document_metadata.get("page_count", 0)
            assert page_count > 0, f"Page count should be > 0, got {page_count}"
            test_logger.log(f"✓ Page count: {page_count}")
            
            # Validate processing metadata
            processing_metadata = response_obj.get("processing_metadata", {})
            assert "parser" in processing_metadata, "Missing parser in processing_metadata"
            assert "extraction_mode" in processing_metadata, "Missing extraction_mode in processing_metadata"
            test_logger.log(f"✓ Extraction mode: {processing_metadata.get('extraction_mode', 'N/A')}")
            
            # Validate extracted community data
            print("\nValidating Extracted Community Data:")
            required_derived_fields = ["communityName", "municipality", "state"]
            for field in required_derived_fields:
                assert field in derived_fields, f"Missing extracted field: {field}"
                assert derived_fields[field] is not None and derived_fields[field] != "", \
                    f"Extracted field '{field}' should not be null or empty"
                print(f"  ✓ {field}: {derived_fields[field]}")
            
            # Validate optional but important fields
            optional_fields = ["division", "numberOfLots", "city", "country"]
            print("\nOptional Fields:")
            for field in optional_fields:
                if field in derived_fields:
                    value = derived_fields[field]
                    if value is not None and value != "":
                        print(f"  ✓ {field}: {value}")
                    else:
                        print(f"  ⚠ {field}: Empty or null")
                else:
                    print(f"  ⚠ {field}: Not present")
            
            # Validate pages structure
            pages = response_obj.get("pages", [])
            assert len(pages) > 0, "Response should contain at least one page"
            assert pages[0].get("page_number") == 1, "First page should be numbered 1"
            test_logger.log(f"✓ Pages structure validated: {len(pages)} pages found")
            
            # Summary statistics
            print("\n" + "-"*80)
            print("DATASET SUMMARY:")
            print(f"  Community Name: {derived_fields.get('communityName', 'N/A')}")
            print(f"  Location: {derived_fields.get('city', 'N/A')}, {derived_fields.get('state', 'N/A')}")
            print(f"  Number of Lots: {derived_fields.get('numberOfLots', 'N/A')}")
            print(f"  Division: {derived_fields.get('division', 'N/A')}")
            print(f"  Processing Time: {document_metadata.get('processing_time', 'N/A')} seconds")
            print(f"  Total Pages: {len(pages)}")
            print(f"  Extraction Mode: {processing_metadata.get('extraction_mode', 'N/A')}")
            print("="*80 + "\n")
            
            test_logger.log("✓ All dataset validations passed")
        else:
            test_logger.log(f"Skipping schema validation for non-200 response: {response.status}")
