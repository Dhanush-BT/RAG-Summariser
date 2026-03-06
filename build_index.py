import os
import uuid
from dotenv import load_dotenv
import pdfplumber  # For reading PDFs
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from tqdm import tqdm  # Progress bars

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Configurations
# -----------------------------
QDRANT_URL = os.getenv("QDRANT_URL", "https://997a6b03-a01e-4165-9feb-7147be910ae8.sa-east-1-0.aws.cloud.qdrant.io")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "static_doc_rag")
PDF_PATH = os.getenv("PDF_PATH", "20AIEL510,Cryptography and Network Security Principles and Practices,William Stallings.pdf")

# Chunking parameters for large PDFs
CHUNK_SIZE = 300   # words per chunk
OVERLAP = 50       # words overlap between chunks
BATCH_SIZE = 64    # points per Qdrant upsert

# -----------------------------
# Embedding model
# -----------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Qdrant client
# -----------------------------
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=False
)

# Create Collection if Not Exists
if not qdrant.collection_exists(COLLECTION_NAME):
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )
    print("Collection created ✅")
else:
    print("Collection already exists ✅")

# -----------------------------
# Read PDF File
# -----------------------------
text = ""
with pdfplumber.open(PDF_PATH) as pdf:
    print(f"Reading PDF: {PDF_PATH} ({len(pdf.pages)} pages)")
    for page in tqdm(pdf.pages, desc="Reading pages"):
        page_text = page.extract_text()
        if page_text and page_text.strip():
            text += page_text.strip() + "\n"

print(f"Total text length: {len(text)} characters")

# -----------------------------
# Chunking Function
# -----------------------------
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Word-based sliding window chunking
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
    return chunks

print("Creating text chunks...")
chunks = chunk_text(text)
print(f"Total chunks created: {len(chunks)}")

# -----------------------------
# Batch Upsert Function
# -----------------------------
def batch_upsert(client, collection, points, batch_size=BATCH_SIZE):
    for i in tqdm(range(0, len(points), batch_size), desc="Indexing batches"):
        client.upsert(
            collection_name=collection,
            points=points[i:i + batch_size]
        )

# -----------------------------
# Vector Encoding + Indexing
# -----------------------------
points = []
print("Encoding chunks into embeddings...")
for i, chunk in tqdm(enumerate(chunks), desc="Encoding chunks", total=len(chunks)):
    if not chunk.strip():
        continue
    vector = embed_model.encode(chunk).tolist()
    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": chunk,
                "chunk_id": i,
                "source": "study_plan_doc"
            },
        )
    )

print("Encoding completed ✅")
print("Starting batch indexing...")
batch_upsert(client=qdrant, collection=COLLECTION_NAME, points=points)
print("Indexing complete ✅")