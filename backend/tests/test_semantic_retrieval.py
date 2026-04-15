from datetime import datetime, timedelta

from app.application.chat_usecase import ChatUseCase
from app.core.embedding.engine import generate_embedding
from app.core.knowledge_graph.extractor import extract_entities
from app.domain.graph.service import GraphService
from app.domain.memory.service import MemoryService, _MEMORY_STORE, save_memory
from app.core.retrieval.semantic import get_relevant_memories
from app.core.inference.classifier import classify_memory


def test_memory_classifier_maps_common_phrases() -> None:
    assert classify_memory("I am building Cognet backend") == "project"
    assert classify_memory("I completed API setup") == "completed"
    assert classify_memory("I need to improve retrieval") == "task"
    assert classify_memory("Hello there") == "general"


def test_save_memory_adds_type_and_timestamp() -> None:
    _MEMORY_STORE.clear()
    record = save_memory("user-1", "I am building Cognet backend", generate_embedding("I am building Cognet backend"))

    assert record["type"] == "project"
    assert isinstance(record["created_at"], datetime)
    assert record["importance"] == 0.9


def test_knowledge_graph_extractor_finds_entities_and_relation() -> None:
    result = extract_entities("I am building Cognet backend")

    assert "Cognet" in result["entities"]
    assert "backend" in result["entities"]
    assert result["relations"][0] == ("user", "working_on", "Cognet")


def test_semantic_retrieval_ranks_relevant_memory_first() -> None:
    query_embedding = generate_embedding("I am building backend for Cognet")
    memories = [
        {
            "content": "Went for a walk outside",
            "embedding": generate_embedding("Went for a walk outside"),
            "created_at": datetime.utcnow() - timedelta(days=7),
        },
        {
            "content": "Building Cognet backend",
            "embedding": generate_embedding("Building Cognet backend"),
            "created_at": datetime.utcnow(),
        },
        {
            "content": "Reviewed unrelated meeting notes",
            "embedding": generate_embedding("Reviewed unrelated meeting notes"),
            "created_at": datetime.utcnow() - timedelta(days=1),
        },
    ]

    top_memories = get_relevant_memories(query_embedding, memories, top_k=1)

    assert top_memories[0]["content"] == "Building Cognet backend"


def test_chat_use_case_builds_context_from_relevant_memories() -> None:
    service = MemoryService(storage=[])
    use_case = ChatUseCase(memory_service=service, graph_service=GraphService())

    service.save_memory("user-1", "I am building Cognet backend", generate_embedding("I am building Cognet backend"))
    service.save_memory("user-1", "I completed API setup", generate_embedding("I completed API setup"))
    service.save_memory("user-1", "I need to improve retrieval", generate_embedding("I need to improve retrieval"))

    result = use_case.handle_chat("user-1", "What should I do next?")

    assert result["context"]["project"] is not None
    assert "Current Project:" in result["formatted_context"]
    assert any("Suggested next step:" in insight for insight in result["insights"])


def test_session_filter_keeps_related_memories_together() -> None:
	service = MemoryService(storage=[])
	service.save_memory("user-1", "Session one project", generate_embedding("Session one project"), session_id="session_1")
	service.save_memory("user-1", "Session two project", generate_embedding("Session two project"), session_id="session_2")

	assert len(service.get_recent_memories("user-1", session_id="session_1")) == 1
	assert service.get_recent_memories("user-1", session_id="session_1")[0]["session_id"] == "session_1"