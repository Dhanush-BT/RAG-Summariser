import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configuration
QDRANT_URL = "https://997a6b03-a01e-4165-9feb-7147be910ae8.sa-east-1-0.aws.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.yUp0jH_r9ULr1cl6xqWOECpxO1ThzGkJh3sErxl5FHc"
CEREBRAS_API_KEY = "csk-9xxfdmrerwjn9wyrx2fye95knrn5dm4n4cv2vr5mfc5f996y"

COLLECTION_NAME = "static_doc_rag"

# Initialize Models
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

client = OpenAI(
    api_key=CEREBRAS_API_KEY,
    base_url="https://api.cerebras.ai/v1"
)

# Retrieval Function
def retrieve(query, k=5):
    """Semantic retrieval from Qdrant"""

    query_vector = embed_model.encode(query).tolist()

    search_result = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=k
    )

    contexts = []

    if search_result and search_result.points:
        for point in search_result.points:
            if point.payload and "text" in point.payload:
                contexts.append(point.payload["text"])

    return contexts

# Answer Generation
def generate_answer(query):

    contexts = retrieve(query)

    if not contexts:
        return "I don't know."

    context_text = "\n\n".join(contexts)

    prompt = f"""
You are a PDF summary assistant.
Your role is to answer ONLY using the provided context.
- Do NOT hallucinate.
- If answer is not found in context → say "I don't know".
Context:
{context_text}
Question:
{query}
Answer:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Generation Error: {str(e)}"

# CLI Chat Loop
if __name__ == "__main__":

    print("RAG System Ready 🚀")

    while True:
        query = input("\nAsk your question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        answer = generate_answer(query)

        print("\nAnswer:\n", answer)