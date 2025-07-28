db = KnittingDB()
db.set("test_pattern", {"yarn": "cotton", "stitches": 100})
print(db.get("test_pattern"))  # Should print the pattern