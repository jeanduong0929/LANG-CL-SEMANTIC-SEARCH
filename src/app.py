import os
import csv
import pprint
import chromadb

from typing import List


def clear_screen():
    """
    Clears the terminal screen.

    This function uses a system call to clear the terminal screen. The command
    differs depending on the operating system: 'cls' for Windows ('nt') and 'clear'
    for Unix/Linux.
    """
    os.system("cls" if os.name == "nt" else "clear")


def read_file_from_folder(folder_name: str) -> List[List[str]]:
    """
    Reads the first .csv file from a specified folder and returns its content.

    The function constructs an absolute path to the specified folder, relative
    to the script's location. It then reads the first CSV file found in this folder
    and returns its contents as a list of rows.

    Parameters:
    folder_name (str): The name of the folder from which to read the .csv file.

    Returns:
    list: A list of rows from the CSV file, where each row is represented as a list.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, "..", folder_name)

    # Check if the folder contains any files
    try:
        file_name = next(
            (f for f in os.listdir(folder_path) if f.endswith(".csv")), None
        )
    except FileNotFoundError:
        return []

    if file_name:
        with open(os.path.join(folder_path, file_name)) as file:
            return list(csv.reader(file))

    return []


def get_embeddings_from_csv(file_data: List[List[str]]) -> tuple:
    """
    Extracts document data, metadata, and IDs from the given CSV file data.

    This function iterates over each line of the CSV file data (excluding the first line),
    extracting the document text, metadata (item ID), and generating a unique ID for each line.
    If a line does not have the required number of elements, it is skipped with a warning.

    Parameters:
    file_data (list of lists): The content of the CSV file, where each inner list represents a line.

    Returns:
    tuple: A tuple containing three lists - documents, metadatas, and ids.
    """
    documents = []
    metadatas = []
    ids = []

    for i, line in enumerate(file_data):
        if i == 0:
            # Skip the first line
            continue

        # Check if the line has enough elements
        if len(line) >= 2:
            documents.append(line[1])
            metadatas.append({"item_id": line[0]})
            ids.append(str(i))
        else:
            print(
                f"Warning: Line {i} in the CSV file is missing data and will be skipped."
            )

    return documents, metadatas, ids


def get_chromadb_collection(
    documents: List, metadatas: List, ids: List
) -> chromadb.Collection:
    """
    Initializes a ChromaDB collection and adds documents, metadata, and ids to it.

    This function creates a new ChromaDB collection named 'semantic-lab' and adds the provided
    documents, metadatas, and ids to it. It returns the initialized ChromaDB collection object.

    Parameters:
    documents (list): A list of document texts to add to the collection.
    metadatas (list): A list of metadata dictionaries corresponding to the documents.
    ids (list): A list of unique identifiers for the documents.

    Returns:
    chromadb.Collection: The initialized and populated ChromaDB collection object.
    """
    chroma_client = chromadb.Client()

    collection = chroma_client.create_collection(
        name="semantic-lab",
    )
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )

    return collection


def main():
    clear_screen()

    print("Embeddings...\n")

    # Read the files from the resources folder
    file_data = read_file_from_folder("resources")

    # Get the embeddings from the csv files
    documents, metadatas, ids = get_embeddings_from_csv(file_data)

    # Initializing the collection
    collection = get_chromadb_collection(documents, metadatas, ids)

    while True:
        clear_screen()

        # Get user input
        user_input = input("Search menu item (x to cancel): ")

        # Check if the user wants to exit
        if user_input == "x":
            break

        # Query the collection
        results = collection.query(query_texts=[user_input], n_results=5)

        # Print the results
        # Note: Remove the 'documents' key if you don't want to print only documents
        pprint.pprint(results["documents"])

        input("\nPress enter to continue...")


if __name__ == "__main__":
    main()
