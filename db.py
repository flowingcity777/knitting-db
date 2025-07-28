class KnittingDB:
    def __init__(self):
        self.data = {}  # Simple dictionary storage

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)