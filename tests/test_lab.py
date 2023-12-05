import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402
from src.app import get_chromadb_collection  # noqa: E402


class ChromaDBTests(unittest.TestCase):
    def test_get_chromadb_collection(self):
        """
        Tests the get_chromadb_collection function. This test checks if the function correctly
        handles existing collections and creates a new one as needed.

        - Mocks the chromadb.Client to simulate the presence of an existing 'test' collection.
        - Verifies that the existing collection is deleted.
        - Confirms that a new collection is created.
        - Asserts that the function returns the expected value after creating the new collection.

        This ensures that the function behaves correctly when managing collections in the database.
        """
        mock_client = MagicMock()
        mock_client.list_collections.return_value = ["test"]
        mock_client.create_collection.return_value = "Collection Created"

        with patch("chromadb.Client", return_value=mock_client):
            collection = get_chromadb_collection()

            mock_client.delete_collection.assert_called_with(name="test")
            mock_client.create_collection.assert_called_with(name="test")
            self.assertEqual(collection, "Collection Created")


if __name__ == "__main__":
    unittest.main()
