"""
MongoDB Integration Service
Demonstrates document-based NoSQL integration alongside SQL.
Used for flexible agricultural telemetry, unstructured field bulletins,
and multi-source ICAR knowledge digests.
Includes graceful fallback if MongoDB instance is not locally active.
"""

import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

_mongo_client = None
_mongo_db = None

def get_mongo_db():
    global _mongo_client, _mongo_db
    if _mongo_db is not None:
        return _mongo_db

    mongo_uri = getattr(settings, 'MONGODB_URI', '') or os.getenv('MONGODB_URI', '')
    if not mongo_uri:
        # Check standard default
        mongo_uri = 'mongodb://localhost:27017/agrismart_mongo'

    try:
        from pymongo import MongoClient
        _mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1000)
        # Test connection
        _mongo_client.admin.command('ping')
        _mongo_db = _mongo_client.get_database()
        logger.info("Connected to MongoDB successfully")
        return _mongo_db
    except Exception as e:
        logger.warning(f"MongoDB not reachable ({e}). Gracefully running in SQL-only mode.")
        return None

def save_document_advisory(article_dict):
    """
    Save unstructured article or ICAR bulletin document to MongoDB collection.
    """
    db = get_mongo_db()
    if db is None:
        return None
    try:
        col = db['agricultural_bulletins']
        res = col.update_one({'slug': article_dict.get('slug')}, {'$set': article_dict}, upsert=True)
        return str(res.upserted_id or 'updated')
    except Exception as e:
        logger.error(f"Failed to write document to MongoDB: {e}")
        return None

def get_document_advisories(category=None, limit=10):
    db = get_mongo_db()
    if db is None:
        return []
    try:
        col = db['agricultural_bulletins']
        query = {'category': category} if category else {}
        cursor = col.find(query, {'_id': 0}).limit(limit)
        return list(cursor)
    except Exception as e:
        logger.error(f"Failed to read from MongoDB: {e}")
        return []

