import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402
from src.app import get_chromadb_collection, get_embeddings_from_csv  # noqa: E402


class ChromaDBTests(unittest.TestCase):
    def test_get_embeddings_from_csv_valid_data(self):
        test_data = [["ID", "Text"], ["1", "Document 1"], ["2", "Document 2"]]
        expected_documents = ["Document 1", "Document 2"]
        expected_metadata = [{"item_id": "1"}, {"item_id": "2"}]
        expected_ids = ["1", "2"]

        documents, metadata, ids = get_embeddings_from_csv(test_data)

        self.assertEqual(documents, expected_documents)
        self.assertEqual(metadata, expected_metadata)
        self.assertEqual(ids, expected_ids)

    def test_get_embeddings_from_csv_incomplete_data(self):
        # Set the test data
        test_data = [["ID", "Text"], ["1"], ["2", "Document 2"]]

        # Set the expected return values
        expected_documents = ["Document 2"]
        expected_metadata = [{"item_id": "2"}]
        expected_ids = ["2"]

        # Call the function to get the actual values
        actual_documents, actual_metadata, actual_ids = get_embeddings_from_csv(
            test_data
        )

        # Assert the actual values are the same as the expected values
        self.assertEqual(actual_documents, expected_documents)
        self.assertEqual(actual_metadata, expected_metadata)
        self.assertEqual(actual_ids, expected_ids)

    @patch("src.app.chromadb.Client")
    def test_get_chromadb_collection(self, mock_chromadb_client):
        # Mock the ChromaDB client and collection
        mock_client = MagicMock()
        mock_collection = MagicMock()

        # Set the return values for the mocked functions
        mock_chromadb_client.return_value = mock_client
        mock_client.create_collection.return_value = mock_collection

        # Set the test data
        documents = ["Document 1", "Document 2"]
        metadatas = [{"item_id": "1"}, {"item_id": "2"}]
        ids = ["1", "2"]

        # Call the function to get the actual values
        actual_collection = get_chromadb_collection(documents, metadatas, ids)

        # Assert of actual_collection is the same as the mocked collection
        self.assertEqual(actual_collection, mock_collection)

        # Assert the mocked functions were called with the correct parameters
        mock_client.create_collection.assert_called_with(name="semantic-lab")

        # Assert the mocked functions were called with the correct parameters
        mock_collection.add.assert_called_with(
            documents=documents, metadatas=metadatas, ids=ids
        )


if __name__ == "__main__":
    unittest.main()
