"""Base repository.

Purpose:
Share common MongoDB repository behavior.
"""

from __future__ import annotations

from abc import ABC
from typing import Any, Mapping

from pymongo.collection import Collection

from app.infrastructure.db.mongo.client import get_collection


class MongoRepository(ABC):
	"""Base helper around a Mongo collection."""

	def __init__(self, collection_name: str) -> None:
		self.collection: Collection = get_collection(collection_name)

	@staticmethod
	def _sanitize(document: Mapping[str, Any] | None) -> dict[str, Any] | None:
		if document is None:
			return None
		sanitized = dict(document)
		sanitized.pop("_id", None)
		return sanitized

	def find_one(self, query: Mapping[str, Any]) -> dict[str, Any] | None:
		"""Return a single document without Mongo metadata."""

		return self._sanitize(self.collection.find_one(dict(query), {"_id": False}))

	def find_many(self, query: Mapping[str, Any], *, limit: int = 50, sort: list[tuple[str, int]] | None = None) -> list[dict[str, Any]]:
		"""Return a list of sanitized documents."""

		cursor = self.collection.find(dict(query), {"_id": False})
		if sort:
			cursor = cursor.sort(sort)
		return [dict(document) for document in cursor.limit(limit)]

	def insert_one(self, document: Mapping[str, Any]) -> dict[str, Any]:
		"""Insert a document and return the stored copy."""

		payload = dict(document)
		result = self.collection.insert_one(payload)
		payload["id"] = str(result.inserted_id)
		return payload

	def ensure_indexes(self, index_fields: list[str]) -> None:
		"""Create single-field indexes for the supplied fields."""

		for field_name in index_fields:
			self.collection.create_index(field_name)
