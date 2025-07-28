from db import KnittingDB  # <-- Add this at the top!

db = KnittingDB()
db.set("test_pattern", {"yarn": "cotton", "stitches": 100})
print(db.get("test_pattern"))