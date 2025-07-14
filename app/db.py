from tinydb import TinyDB, Query
from pathlib import Path

db = TinyDB(Path("users.json"))
UserQuery = Query()
