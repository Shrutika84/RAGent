import os
import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from app.config import settings

# Load embedding model
embedder = SentenceTransformer(settings.EMBEDDING_MODEL)

index_path = settings.VECTOR_STORE_PATH
embedding_path = index_path.replace(".faiss", ".pkl")

# chunks
columns_to_include = [
    "Property Address", "Floor", "Suite", "Size (SF)",
    "Rent/SF/Year", "Annual Rent", "Monthly Rent", "GCI On 3 Years",
    "Associate 1", "Associate 2", "Associate 3", "Associate 4"
]

def row_to_text(row) -> str:
    return (
        f"Property: {row['Property Address']}, Suite {row['Suite']}, Floor {row['Floor']}, "
        f"Size: {row['Size (SF)']} SF, Rent/SF: {row['Rent/SF/Year']}, "
        f"Annual Rent: {row['Annual Rent']}, Monthly Rent: {row['Monthly Rent']}, "
        f"GCI (3 Years): {row['GCI On 3 Years']}, Brokers: "
        f"{row['Associate 1']}, {row['Associate 2']}, {row['Associate 3']}, {row['Associate 4']}"
    )

def load_and_index_documents():
    # FAISS check
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    csv_path = os.path.abspath(settings.DOC_EMBED_CSV)
    print(f"📄 Loading CSV from: {csv_path}")
    df = pd.read_csv(csv_path)

    # df = pd.read_csv(settings.DOC_EMBED_CSV)
    texts = df.apply(row_to_text, axis=1).tolist()
    embeddings = embedder.encode(texts, show_progress_bar=True)

    # Save FAISS index
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, index_path)

    with open(embedding_path, "wb") as f:
        pickle.dump(texts, f)

    print(f"✅ Indexed {len(texts)} property entries into FAISS.")

def retrieve_relevant_chunks(query: str, top_k: int = 3) -> str:
    if not os.path.exists(index_path) or not os.path.exists(embedding_path):
        return "Upload documents please."

    index = faiss.read_index(index_path)
    with open(embedding_path, "rb") as f:
        texts = pickle.load(f)

    query_vec = embedder.encode([query])
    D, I = index.search(query_vec, top_k)
    return "\n\n".join([texts[i] for i in I[0]])
