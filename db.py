import json

class KnittingDB:
    def __init__(self, storage_file="knitting_db.json"):
        self.storage_file = storage_file
        self.data = {}
        self._load_from_disk()  # Load existing data on startup

    def _load_from_disk(self):
        try:
            with open(self.storage_file, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}  # Start fresh if file doesn't exist/corrupt

    def _save_to_disk(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.data, f)

    # ===== User-facing methods =====
    def set(self, key, value):
        self.data[key] = value
        self._save_to_disk()  # Auto-save on every change

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save_to_disk()
            return f"Deleted: {key}"
        return "❌ Key not found"