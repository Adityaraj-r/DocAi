import json
import threading
from app.core.config import settings
from app.core.logger import logger
from app.services.ingestion import IngestionService
from app.services.rag_pipeline import RAGPipelineService
from app.redis_pubsub.client import create_redis_client

def start_redis_listener():
    def listen_loop():
        logger.info(f"Connecting Python AI Service Redis Listener to {settings.redis_host}:{settings.redis_port}")
        r = create_redis_client()
        pubsub = r.pubsub()
        pubsub.subscribe("doc:ingest:request", "chat:stream:request")

        logger.info("Subscribed to 'doc:ingest:request' and 'chat:stream:request' Redis channels")

        for item in pubsub.listen():
            if item["type"] == "message":
                channel = item["channel"]
                try:
                    data = json.loads(item["data"])
                    logger.info(f"Received Redis Pub/Sub task on channel '{channel}'")

                    if channel == "doc:ingest:request":
                        IngestionService.ingest_pdf(
                            document_id=data["documentId"],
                            file_path=data["fileUrl"],
                            collection_name=data["vectorCollectionId"]
                        )

                    elif channel == "chat:stream:request":
                        RAGPipelineService.process_chat_query(
                            request_id=data["requestId"],
                            conversation_id=data["conversationId"],
                            query=data["query"],
                            collection_name=data["vectorCollectionId"]
                        )
                except Exception as e:
                    logger.error(f"Error handling Redis event on {channel}: {e}")

    thread = threading.Thread(target=listen_loop, daemon=True)
    thread.start()
    logger.info("Background Redis Pub/Sub listener thread started")
