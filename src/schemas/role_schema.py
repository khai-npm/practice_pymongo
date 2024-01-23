import sys
sys.path.append("./src/models/")
from role import role
import pymongo
from permission_schema import permission_schema
from bson import ObjectId

class role_schema:
    
    def __init__(self):
        self.Session = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.Session["authenication_database"]
        self.role_col = self.database["roles"]

        count = len(list(self.role_col.find()))
        if count == 0:
            newrole = role(role_name="admin", permissions=["All"])
            newrole2 = role(role_name="user", permissions=["base_user", "user_permission_sample_add"])
            self.role_col.insert_one({
                                        "role_name" : newrole.role_name,
                                        "permissions" : newrole.permissions})
            self.role_col.insert_one({
                                        "role_name" : newrole2.role_name,
                                        "permissions" : newrole2.permissions})
            
    def get_all_role(self):
        db = self.role_col.find()
        if db is None:
            return None
        result : list = []
        for i in db:
            _id = str(i['_id'])
            role_name = i['role_name']
            permissions = i['permissions']

            a = {
                "_id" : _id,
                "role_name" : role_name,
                "permissions" : permissions
            }

            result.append(a)

        return result
    

    def get_role_by_id(self, id):
        db = self.role_col.find_one({"_id" : ObjectId(id)})
        if db is None:
            return None

        for i in db:
            _id = str(db['_id'])
            role_name=db['role_name']
            permissions=db['permissions']

            result = {
                "_id" : _id,
                "role_name" : role_name,
                "permissions" : permissions
            }

        
        return result
    
    def get_role_by_name(self, role_name):
        db = self.role_col.find_one({"role_name" : role_name})
        if db is None:
            return None

        for i in db:
            _id = str(db['_id'])
            role_name=db['role_name']
            permissions=db['permissions']

            result = {
                "_id" : _id,
                "role_name" : role_name,
                "permissions" : permissions
            }

        
        return result
    
    def generate_role_id(self):
        i = len(self.get_all_role())
        flag = False
        while flag is False:
            new_id = "rid_"+ str(i)
            if self.get_role_by_id(new_id) is not None:
                i = i + 1
            else:
                flag = True
                return new_id
            
    def add_new_role(self, new_role : role):
        new_role.role_name = new_role.role_name.replace(" ", "").lower()
        for i in new_role.permissions:
            i = i.replace(" ", "")
        per_db = permission_schema()
        try:
            if self.role_col.find_one({"role_name" : new_role.role_name}) is not None:
                raise ValueError('role name existed !')
            
            
            for i in new_role.permissions:
                if i not in per_db.get_per_list():
                    raise ValueError('a permission not in system')
            
            self.role_col.insert_one({
                                            "role_name" : new_role.role_name,
                                            "permissions" : new_role.permissions
                                    })

        except ValueError as e:
            raise ValueError('Error at add_new_role() :', str(e))

    def update_role(self, roleid, new_role : role):
        new_role.role_name = new_role.role_name.replace(" ", "")
        for i in new_role.permissions:
            i = i.replace(" ", "")
        per_db = permission_schema()
        try:
            
            if self.get_role_by_id(roleid) is None:
                raise ValueError('role does not exist')
            
            for i in new_role.permissions:
                if i not in per_db.get_per_list():
                    raise ValueError('a permission not in system')
            find_role = {"_id" : ObjectId(roleid)}
            update_value = {"$set" : {"role_name" : new_role.role_name, "permissions" : new_role.permissions}}

            self.role_col.update_one(find_role, update_value)
        except ValueError as e:
            raise ValueError("error at update_role() : " + str(e))






