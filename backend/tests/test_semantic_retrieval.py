from app.application.chat_usecase import ChatUseCase
from app.core.embedding.engine import generate_embedding
from app.core.retrieval.semantic import get_relevant_memories


def test_semantic_retrieval_ranks_relevant_memory_first() -> None:
    query_embedding = generate_embedding("I am building backend for Cognet")
    memories = [
        {"content": "Went for a walk outside", "embedding": generate_embedding("Went for a walk outside")},
        {"content": "Building Cognet backend", "embedding": generate_embedding("Building Cognet backend")},
        {"content": "Reviewed unrelated meeting notes", "embedding": generate_embedding("Reviewed unrelated meeting notes")},
    ]

    top_memories = get_relevant_memories(query_embedding, memories, top_k=1)

    assert top_memories[0]["content"] == "Building Cognet backend"


def test_chat_use_case_builds_context_from_relevant_memories() -> None:
    def memory_loader(user_id: str, limit: int):
        return [
            {"content": "Building Cognet backend", "embedding": generate_embedding("Building Cognet backend")},
            {"content": "Doing grocery shopping", "embedding": generate_embedding("Doing grocery shopping")},
        ][:limit]

    use_case = ChatUseCase(memory_loader=memory_loader)
    result = use_case.handle_chat("user-1", "I am building backend for Cognet")

    assert result["context"]["project"] == "Building Cognet backend"
    assert "Current Project:" in result["formatted_context"]
    assert any("Suggested next step:" in insight for insight in result["insights"])
    assert result["relevant_memories"][0]["content"] == "Building Cognet backend"