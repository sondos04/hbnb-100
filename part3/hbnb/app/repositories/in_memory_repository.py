class InMemoryRepository:
    def __init__(self):
        self._data = {}
    
    def add(self, entity):
        self._data[entity.id] = entity
    
    def get(self, entity_id):
        return self._data.get(entity_id)
    
    def get_all(self):
        return list(self._data.values())
    
    def update(self, entity_id, entity):
        if entity_id in self._data:
            self._data[entity_id] = entity
            return True
        return False
    
    def delete(self, entity_id):
        if entity_id in self._data:
            del self._data[entity_id]
            return True
        return False
