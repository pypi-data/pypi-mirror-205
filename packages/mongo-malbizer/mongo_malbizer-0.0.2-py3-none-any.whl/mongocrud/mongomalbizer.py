from pymongo import MongoClient
import pymongo

class MongoCRUD():
    def __init__(self, location, collection, port = 27017):
        self.client = MongoClient(location, port)
        self.db = self.client[collection]
        
    def insert(self,table,value):
        try:
            collection = self.db[table]
            _id = collection.insert_one(value).inserted_id
            return _id
        except Exception as e:
            return None
        
    def insert_or_update(self,table, idvalue, value):
        try:
            _id = self.update_one(table, idvalue, value)
            if _id == None:
                value['_id'] = idvalue
                _id = self.insert(table, value)
            return _id
        except Exception as e:
            print(e)
            return None
    
    def insert_list(self, table, listvalues):
        try:
            if(isinstance(listvalues,dict)):
                return self.insert(table,listvalues)
            collection = self.db[table]
            _ids = collection.insert_many(listvalues).inserted_ids
            return _ids
        except Exception as e:
            return []
    
    def select_one(self, table, query, columns=None):
        try:
            collection = self.db[table]
            if columns:
                values = collection.find_one(query,columns)
            else:
                values = collection.find_one(query)
            return values
        except Exception as e:
            return None
        
    def select(self, table, query={}, columns=None, orderby=None, direction = pymongo.DESCENDING, limit=None):
        try:
            collection = self.db[table]
            if not columns:
                c = collection.find(query)
            else:
                c = collection.find(query, columns)
            if orderby:
                c = c.sort(orderby, direction)
            if limit:
                c = c.limit(limit)
            return [doc for doc in c]
        except Exception as e:
            return None
    
    def update_one(self, table, id, value):
        try:
            collection = self.db[table]
            _id = collection.replace_one({"_id": id}, value).upserted_id
            return _id
        except Exception as e:
            return None
    
    def update_by_id(self, table, ids, values):
        try:
            collection = self.db[table]
            _id = collection.update_many({"_id":{"$in": ids}},values)
            return _id
        except Exception as e:
            print(e)
            return None
        
    def getTables(self):
        try:
            return self.db.list_collection_names()
        except Exception as e:
            return None