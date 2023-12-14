import unittest
from unittest.mock import MagicMock, mock_open, patch
from src.main.app import (
    get_chromadb_collection,
    get_embeddings_from_csv,
    read_file_from_folder,
)


class ChromaDBTests(unittest.TestCase):
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    @patch("os.listdir")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="data1,data2\ndata3,data4"
    )
    def test_read_file_with_existing_csv(
        self, mock_open, mock_listdir, mock_abspath, mock_dirname
    ):
        # Set the mock return values
        mock_dirname.return_value = "/test"
        mock_abspath.return_value = "/test"
        mock_listdir.return_value = ["test.csv"]

        # Call the function to get the actual values
        result = read_file_from_folder("dummy_folder")

        # Assert the actual values are the same as the expected values
        self.assertEqual(result, [["data1", "data2"], ["data3", "data4"]])

    @patch("os.path.dirname")
    @patch("os.path.abspath")
    @patch("os.listdir")
    def test_read_file_folder_not_found(self, mock_listdir, mock_abspath, mock_dirname):
        # Set the mock return values
        mock_dirname.return_value = "/test"
        mock_abspath.return_value = "/test"
        mock_listdir.side_effect = FileNotFoundError

        # Call the function to get the actual values
        result = read_file_from_folder("nonexistent_folder")

        # Assert the actual values are the same as the expected values
        self.assertEqual(result, [])

    @patch("os.path.dirname")
    @patch("os.path.abspath")
    @patch("os.listdir")
    def test_read_file_no_csv_in_folder(self, mock_listdir, mock_abspath, mock_dirname):
        # Set the mock return values
        mock_dirname.return_value = "/test"
        mock_abspath.return_value = "/test"
        mock_listdir.return_value = ["test.txt", "test.doc"]

        # Call the function to get the actual values
        result = read_file_from_folder("empty_csv_folder")

        # Assert the actual values are the same as the expected values
        self.assertEqual(result, [])

    def test_get_embeddings_from_csv_valid_data(self):
        # Set the test data
        test_data = [["ID", "Text"], ["1", "Document 1"], ["2", "Document 2"]]

        # Set the expected return values
        expected_documents = ["Document 1", "Document 2"]
        expected_metadata = [{"item_id": "1"}, {"item_id": "2"}]
        expected_ids = ["1", "2"]

        # Call the function to get the actual values
        acutal_documents, actual_metadata, actual_ids = get_embeddings_from_csv(
            test_data
        )

        # Assert the actual values are the same as the expected values
        self.assertEqual(acutal_documents, expected_documents)
        self.assertEqual(actual_metadata, expected_metadata)
        self.assertEqual(actual_ids, expected_ids)

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
