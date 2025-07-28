# Knitting Pattern Database 🧶

A minimal database for storing and retrieving knitting patterns.

## Features
- Key-value storage
- Simple API (`set`, `get`, `delete`)
- Lightweight and easy to integrate

## Usage
```python
from db import KnittingDB
db = KnittingDB()
db.set("sweater123", {"yarn": "wool", "stitches": 200})