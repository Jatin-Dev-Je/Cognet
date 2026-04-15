from app.core.events.event_bus import event_bus
from app.domain.connectors.github_connector import GitHubConnector
from app.domain.memory.service import MemoryService, _MEMORY_STORE
from app.core.embedding.engine import generate_embedding


def test_github_connector_processes_mock_activity() -> None:
	connector = GitHubConnector()

	data = connector.fetch_data()
	processed = connector.process(data)

	assert data
	assert processed[0]["type"] == "activity"
	assert processed[0]["content"] == data[0]


def test_event_bus_delivers_payload_to_subscriber() -> None:
	event_bus.listeners.clear()
	received = []

	event_bus.subscribe("platform_event", lambda payload: received.append(payload))
	event_bus.publish("platform_event", {"status": "ok"})

	assert received == [{"status": "ok"}]


def test_memory_save_publishes_created_event() -> None:
	_MEMORY_STORE.clear()
	event_bus.listeners.clear()
	received = []
	event_bus.subscribe("memory_created", lambda payload: received.append(payload["content"]))

	service = MemoryService(storage=[])
	service.save_memory("user-1", "Connected GitHub mock", generate_embedding("Connected GitHub mock"))

	assert received == ["Connected GitHub mock"]
