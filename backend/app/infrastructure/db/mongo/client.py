"""MongoDB client.

Purpose:
Create a single MongoDB connection path for the backend.
"""

from __future__ import annotations

from functools import lru_cache

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.config.settings import get_settings


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient:
	"""Return a cached Mongo client."""

	settings = get_settings()
	return MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)


@lru_cache(maxsize=1)
def get_mongo_database() -> Database:
	"""Return the configured Mongo database."""

	client = get_mongo_client()
	database = client.get_default_database()
	if database is None:
		database = client["cognet"]
	return database


def get_collection(name: str) -> Collection:
	"""Return a Mongo collection by name."""

	return get_mongo_database()[name]
