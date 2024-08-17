import json
import logging
import re
import uuid
from tinydb import Query, TinyDB

from src.config import Settings

settings = Settings()
logger = logging.getLogger(__name__)


class CRUD:
    def __init__(self, db_path: str):
        """
        Init CRUD class with a provided database path
        
        Parameters
        ----------
        db_path : str
            path to TinyDB database file
        """
        try:
            self.db = TinyDB(path=db_path, indent=4, separators=(",", ": "), encoding="utf-8")
            self.query = Query()
            logger.info(f"CRUD init OK with db: {db_path}")
        
        except (IOError, OSError) as e:
            logger.error(f"IO error during CRUD init: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during CRUD init: {e}")
            raise


    def init_db(self, init_data_path):
        """
        Adds data in bulk from a source JSON file
        
        Parameters
        ----------
        init_data_path : str
            path to the source JSON file
        """
        try :
            with open(init_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                self.create_one(item)
            logger.info(f"Data load OK: {init_data_path}")
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
        except PermissionError as e:
            logger.error(f"Permission denied: {e}")
        except (IOError, OSError) as e:
            logger.error(f"IO error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error {e}")


    def create_one(self, item: dict):
        """
        Creates one database item
        Skips item if item._id already in database
        
        Parameter
        ---------
        item : dict
            item to create in database
        """
        try:
            if "_id" not in item:
                item["_id"] = str(uuid.uuid4())
            if self.find("_id", item["_id"]):
                logger.debug(f"Item _id already in db: {item["_id"]}")
            else:
                self.db.insert(item)
                logger.info(f"Item create OK for _id: {item["_id"]}")
        
        except (TypeError, ValueError) as e:
            logger.error(f"Item create error for _id {item.get("_id", "unknown")}: {e}")
        except Exception as e:
            logger.error(f"Unexpected item create error for _id {item.get("_id", "unknown")}: {e}")


    def read_all(self) -> list[dict]:
        """
        Reads and returns all database items
        
        Returns
        -------
        items : list[dict]
            list of all database items
        """
        try:
            items = self.db.all()
            logger.info(f"Read all items OK: {len(items)} items retrieved")
            return items
        
        except Exception as e:
            logger.error(f"Unexpected read all items error: {e}")


    def find(self, key: str, value: str) -> list[dict]:
        """
        Finds database items with the given key-value pair
        
        Parameters
        ----------
        key : str
            key attribute to search for in database
        
        value : str
            value to match against specified key
            
        Returns
        -------
        results : list[dict]
            list of database items that match the find query
        """
        try:
            q = getattr(self.query, key)
            results = self.db.search(q == value)
            logger.debug(f"Item find OK for key='{key}', value='{value}': {len(results)} matches found")
            return results
    
        except AttributeError as e:
            logger.error(f"Item find error for invalid query key '{key}': {e}")
        except TypeError as e:
            logger.error(f"Item find TypeError for query key='{key}', value='{value}': {e}")
        except Exception as e:
            logger.error(f"Unexpected item find error for query key='{key}', value='{value}': {e}")


    def search(self, key: str, value: str) -> list[dict]:
        """
        Performs case-insensitive search for database items
        
        Parameters
        ----------
        key : str
            key attribute to search for in database
        
        value : str
            value to match against specified key
            
        Returns
        -------
        results : list[dict]
            list of database items that match the search query
        """
        try:
            q = getattr(self.query, key)
            results = self.db.search(q.search(f"{value}+", flags=re.IGNORECASE))
            logger.debug(f"Item search OK for key='{key}', value='{value}': {len(results)} matches found")
            return results
        
        except AttributeError as e:
            logger.error(f"Item search error for invalid query key '{key}': {e}")
        except re.error as e:
            logger.error(f"Item search Regex error query key='{key}', value='{value}': {e}")
        except TypeError as e:
            logger.error(f"Item search TypeError for query key='{key}', value='{value}': {e}")
        except Exception as e:
            logger.error(f"Unexpected item search error for query key='{key}', value='{value}': {e}")


    def update_one(self, item_id: str, updated_fields: dict):
        """
        Updates field(s) for one database item based on its _id
        
        Parameters
        ----------
        item_id : str
            _id of item to update in database
        
        updated_fields : dict
           fields to update for this item
        """
        try:
            item_in_db = self.db.search(self.query._id == item_id)
            if item_in_db:
                self.db.update(updated_fields, self.query._id == item_id)
                logger.info(f"Item update OK for _id: {item_id}")
            else:
                logger.info(f"Item update error for _id {item_id}: not found")
            
        except (TypeError, ValueError) as e:
            logger.error(f"Item update error for _id {item_id}: {e}")
        except Exception as e:
            logger.error(f"Unexpected item update error for _id {item_id}: {e}")


    def delete_one(self, item_id: str):
        """
        Deletes one database item based on its _id
        
        Parameters
        ----------
        item_id : str
            _id of item to delete from database
        """
        try:
            item_in_db = self.db.search(self.query._id == item_id)
            if item_in_db:
                self.db.remove(self.query._id == item_id)
                logger.info(f"Item delete OK for _id: {item_id}")
            else:
                logger.info(f"Item delete error for _id {item_id}: not found")
        
        except Exception as e:
            logger.error(f"Unexpected item delete error for _id {item_id}: {e}")


if __name__ == "__main__":
    db_path = str(settings.DATA_DIR / settings.DATABASE)
    init_data_path = str(settings.DATA_DIR / settings.RAW_DATA)
    db = CRUD(db_path=db_path)
    db.init_db(init_data_path=init_data_path)
    events = db.read_all()
    
    all_items = db.read_all()
    print(all_items)
