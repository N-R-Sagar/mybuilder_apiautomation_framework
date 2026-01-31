"""Payload builder for intelligent-builder-intake API requests.

Constructs query parameters dynamically based on test data.
"""
from typing import Dict, Any
from tests.test_data import get_test_case


class PayloadBuilder:
    """Builds API request payloads dynamically."""

    @staticmethod
    def build_query_params(file_id: str) -> Dict[str, Any]:
        """Build query parameters for a given file_id.
        
        Args:
            file_id: The file identifier to build parameters for
            
        Returns:
            dict: Query parameters ready to send to API
            
        Raises:
            ValueError: If file_id not found in test data
        """
        test_case = get_test_case(file_id)
        if not test_case:
            raise ValueError(f"Test case not found for file_id: {file_id}")
        
        return {
            "file_url": test_case["file_url"],
            "file_type": test_case["file_type"],
            "file_id": test_case["file_id"],
            "builder_id": test_case["builder_id"],
            "entity_id": test_case["entity_id"],
        }

    @staticmethod
    def build_query_params_custom(
        file_url: str,
        file_type: str,
        file_id: str,
        builder_id: str,
        entity_id: str,
    ) -> Dict[str, Any]:
        """Build query parameters with custom values.
        
        Args:
            file_url: URL to the file to process
            file_type: Type of file (e.g., community, zoning, blueprint)
            file_id: Unique file identifier
            builder_id: Builder identifier
            entity_id: Entity identifier
            
        Returns:
            dict: Query parameters ready to send to API
        """
        return {
            "file_url": file_url,
            "file_type": file_type,
            "file_id": file_id,
            "builder_id": builder_id,
            "entity_id": entity_id,
        }
