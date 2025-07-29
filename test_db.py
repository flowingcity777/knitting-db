from db import KnittingDB  # <-- Add this at the top!

db = KnittingDB()
db.set("cozy_sweater", {"yarn": "wool", "stitches": 200})
print(db.get("cozy_sweater"))  # Should print the pattern

# Simulate a restart
new_db = KnittingDB()
print(new_db.get("cozy_sweater"))