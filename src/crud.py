import json
import re
import uuid
from tinydb import Query, TinyDB

from src.config import Settings

settings = Settings()


class CRUD:
    def __init__(self, db_path: str):
        self.db = TinyDB(path=db_path, indent=4, separators=(",", ": "), encoding="utf-8")
        self.query = Query()
        self.init_db()
        
    def init_db(self):
        data_path = str(settings.DATA_DIR / settings.RAW_DATA)
        try :
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                self.add_item(item)
        except FileNotFoundError as e:
            print(e)
        
    def add_item(self, item: dict):
        if "_id" not in item:
            item["_id"] = str(uuid.uuid4())
        if not self.find("_id", item["_id"]):
            self.db.insert(item)

    def all_items(self):
        return self.db.all()

    def find(self, key: str, value: str):
        q = getattr(self.query, key)
        return self.db.search(q == value)

    def search(self, key: str, value: str):
        q = getattr(self.query, key)
        return self.db.search(q.search(f"{value}+", flags=re.IGNORECASE))

    def update_item(self, item_id: str, updated_fields: dict):
        self.db.update(updated_fields, self.query._id == item_id)

    def delete_item(self, item_id: str):
        self.db.remove(self.query._id == item_id)
        
    
if __name__ == "__main__":
    db_path = str(settings.DATA_DIR / settings.DATABASE)
    crud = CRUD(db_path=db_path)
    
    data_path = str(settings.DATA_DIR / settings.RAW_DATA)
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for item in data:
        crud.add_item(item)
    
    all_items = crud.all_items()
    print(all_items)
