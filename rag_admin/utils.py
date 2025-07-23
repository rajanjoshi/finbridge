from vertexai import rag
from google.cloud import storage
from google.api_core.exceptions import NotFound
import vertexai
import os
from django.conf import settings

# Configuration
BUCKET_NAME = "vertex_store_bucket"
EMBEDDING_MODEL = "publishers/google/models/text-multilingual-embedding-002"
GCS_PATH = f"gs://{BUCKET_NAME}/rag_docs/"
CORPUS_NAME = f"projects/{settings.GCP_PROJECT_ID}/locations/{settings.GCP_REGION}/ragCorpora/{settings.VERTEX_RAG_CORPUS_ID}"
vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)

def get_or_create_corpus():
    try:
        print("get_or_create_corpus")
        print(CORPUS_NAME)
        rag.get_corpus(CORPUS_NAME)
        print(f"✅ Corpus already exists: {settings.VERTEX_RAG_CORPUS_ID}")
        return settings.VERTEX_RAG_CORPUS_ID
    except Exception as e:
        print("🔨 Creating RAG corpus...")
        corpus = rag.create_corpus(
            display_name="FI Multilingual Corpus",
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=rag.RagEmbeddingModelConfig(
                    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                        publisher_model=EMBEDDING_MODEL
                    )
                )
            ),
        )
        print(f"🔨 RAG corpus created. {corpus.name}")
        corpus_id = corpus.name.split("/")[-1]
        print(corpus_id)   
        return corpus_id

def upload_to_vertex_rag(local_path):
    try:
        file_name = os.path.basename(local_path)
        destination_blob = f"rag_docs/{file_name}"
        storage.Client().bucket(BUCKET_NAME).blob(destination_blob).upload_from_filename(local_path)
        print(f"📤 Uploaded {file_name} to GCS bucket: {BUCKET_NAME}")
        return True
    except Exception as e:
        print("❌ Upload to GCS failed:", e)
        return False

def sync_to_rag():
    try:
        corpus_id = get_or_create_corpus()
        print("🔁 Importing documents from GCS to RAG corpus...")
        GENERATED_CORPUS_NAME = f"projects/{settings.GCP_PROJECT_ID}/locations/{settings.GCP_REGION}/ragCorpora/{corpus_id}"
        print(GENERATED_CORPUS_NAME)
        rag.import_files(
            corpus_name=GENERATED_CORPUS_NAME,
            paths=[GCS_PATH],
            transformation_config=rag.TransformationConfig(
                chunking_config=rag.ChunkingConfig(chunk_size=1024, chunk_overlap=100)
            ),
            max_embedding_requests_per_min=900
        )
        print("✅ RAG sync complete.")
        return True
    except Exception as e:
        print("❌ Sync to RAG failed:", e)
        return False
