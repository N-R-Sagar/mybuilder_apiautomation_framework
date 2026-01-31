"""Test data for intelligent-builder-intake API testing.

Defines parameterized test cases with multiple file types, builders, and entities.
"""

# Test data combinations: (file_url, file_type, file_id, builder_id, entity_id)
TEST_CASES = [
    {
        "file_url": "https://dc-eastus-dev-fs-func-001.azurewebsites.net/api/files/mybldr/projects/6576/files/875c043f-8312-4ead-838a-82181b9e1a5a",
        "file_type": "community",
        "file_id": "abcd1234",
        "builder_id": "example",
        "entity_id": "abcd1234",
        "description": "Community guide PDF for Builder Alpha",
    },
    {
        "file_url": "https://example.com/zoning-map.pdf",
        "file_type": "zoning",
        "file_id": "abcd1234",
        "builder_id": "example",
        "entity_id": "abcd1234",
        "description": "Zoning map PDF for Builder Beta",
    },
    {
        "file_url": "https://example.com/floorplan.png",
        "file_type": "image",
        "file_id": "abcd1234",
        "builder_id": "example",
        "entity_id": "abcd1234",
        "description": "Floor plan image for Builder Gamma",
    },
    {
        "file_url": "https://example.com/blueprint.docx",
        "file_type": "blueprint",
        "file_id": "abcd1234",
        "builder_id": "example",
        "entity_id": "abcd1234",
        "description": "Blueprint document for Builder Delta",
    },
    {
        "file_url": "https://example.com/brochure.pdf",
        "file_type": "brochure",
        "file_id": "abcd1234",
        "builder_id": "example",
        "entity_id": "abcd1234",
        "description": "Marketing brochure for Builder Epsilon",
    },
]


def get_test_case(file_id):
    """Get test case by file_id.
    
    Args:
        file_id: The file identifier to look up
        
    Returns:
        dict: Test case data or None if not found
    """
    for case in TEST_CASES:
        if case["file_id"] == file_id:
            return case
    return None


def get_all_test_cases():
    """Get all test cases.
    
    Returns:
        list: All test case dictionaries
    """
    return TEST_CASES


def get_test_case_ids():
    """Get test case IDs for pytest parameterization.
    
    Returns:
        list: List of file_id strings suitable for pytest.param()
    """
    return [case["file_id"] for case in TEST_CASES]
