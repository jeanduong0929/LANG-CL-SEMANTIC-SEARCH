import chromadb


def get_chromadb_collection():
    """
    Initializes a collection named 'test' in the chromadb database.
    If the collection already exists, it is deleted and then recreated.
    This ensures that a fresh instance of the collection is always available
    at the start of this function. The created collection is then returned.
    """
    chroma_client = chromadb.Client()

    if "test" in chroma_client.list_collections():
        chroma_client.delete_collection(name="test")
    collection = chroma_client.create_collection(name="test")

    return collection


def main():
    collection = get_chromadb_collection()
    print(f"Collection: {collection}")


if __name__ == "__main__":
    main()
