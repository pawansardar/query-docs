from app.db.vector.document_store import DocumentVectorStore

class Debugger:
    def __init__(self, store: DocumentVectorStore):
        self.store = store
    
    def get_collection_points(self):
        return self.store.get_all_points_debug()
    