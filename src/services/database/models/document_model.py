from datetime import datetime
from clients.mongodb.mongodb_client import MongoDBClient

class Document:
    collection_name = "documents"

    def __init__(self, title: str, content: str, source: str = None, metadata: dict = None, _id=None):
        self._id = _id
        self.title = title
        self.content = content
        self.source = source or "unknown"
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data.get('title'),
            content=data.get('content'),
            source=data.get('source'),
            metadata=data.get('metadata', {}),
            _id=data.get('_id')
        )

    def to_dict(self):
        data = {
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self._id is not None:
            data['_id'] = self._id
        return data

    @staticmethod
    def create_document(db_client: MongoDBClient, title: str, content: str, source: str = None, metadata: dict = None):
        # Get next sequential ID
        counters_collection = db_client.get_collection('counters')
        counter = counters_collection.find_one_and_update(
            {'_id': 'document_id'},
            {'$inc': {'seq': 1}},
            upsert=True,
            return_document=True
        )
        doc_id = counter['seq']

        doc = Document(title, content, source, metadata, _id=doc_id)
        collection = db_client.get_collection(Document.collection_name)
        result = collection.insert_one(doc.to_dict())
        return doc

    @staticmethod
    def find_documents_by_content(db_client: MongoDBClient, search_text: str):
        collection = db_client.get_collection(Document.collection_name)
        # Simple text search - in production, use text indexes
        data_list = collection.find({'content': {'$regex': search_text, '$options': 'i'}})
        return [Document.from_dict(data) for data in data_list]

    @staticmethod
    def find_document_by_id(db_client: MongoDBClient, doc_id):
        collection = db_client.get_collection(Document.collection_name)
        data = collection.find_one({'_id': doc_id})
        if data:
            return Document.from_dict(data)
        return None

    @staticmethod
    def get_all_documents(db_client: MongoDBClient):
        collection = db_client.get_collection(Document.collection_name)
        data_list = collection.find({})
        return [Document.from_dict(data) for data in data_list]