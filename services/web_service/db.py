from tinydb import TinyDB, Query
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / "web_service" / "users.json"
db = TinyDB(db_path)
UserQuery = Query()
