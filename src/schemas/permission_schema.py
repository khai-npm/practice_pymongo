import json
import sys
sys.path.append("./src/models/")
from permission import permission
import pymongo

class permission_schema:
    def __init__(self):
        file = open("./src/settings/appsettings.json")
        data = json.load(file)

        connection_string = data['connection_string']['default_connection_string']
        self.Session = pymongo.MongoClient(connection_string)
        self.database = self.Session["authenication_database"]
        self.permission_col = self.database["permissions"]
        
        count = len(list(self.permission_col.find()))
        if count == 0:
            newper = permission(permission_name="all")
            newper2 = permission(permission_name="base_user")
            self.permission_col.insert_one({"permission_name" : newper.permission_name})
            self.permission_col.insert_one({"permission_name" : newper2.permission_name})

        
    def get_per_list(self):
        db = self.permission_col.find()
        perlist : list =[]
        for i in db:
            permission = i['permission_name']
            perlist.append(permission)

        return perlist
    

    def add_new_per(self, pername : permission):
        pername.permission_name = pername.permission_name.replace(" ", "").lower()
        try:
            if pername.permission_name == "":
                raise ValueError('permission field must not be null')
            if pername.permission_name in self.get_per_list():
                raise ValueError('permission already exist')
            self.permission_col.insert_one({"permission_name" : pername.permission_name})
        except ValueError as e:
            raise ValueError('Error at Add_New_per(): ' + str(e))
