import sys
sys.path.append("./src/models/")
sys.path.append("./src/routers/utils")
from user import user
from password_hash_util import hash_password
from bson import ObjectId
from role_schema import role_schema


import pymongo

class user_schema:
    def __init__(self):
        self.roledb = role_schema()
        self.hash_util = hash_password()
        self.Session = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.Session["authenication_database"]
        self.user_col = self.database["users"]
        
        if len(list(self.user_col.find())) == 0:
            self.user_col.insert_one({
                "user_name" : "admin",
                "password" : self.hash_util.DoHashPassword("1"),
                "role" : "admin",
                "full_name" : "admin account",
                "phone_number" : "000000000",
                "description" : "this is admin account"
            })    

    def get_user_list(self):
        db = self.user_col.find()
        result_list : list = []
        
        for i in db:
            _id = str(i['_id'])
            user_name = i['user_name']
            role = i['role']
            full_name = i['full_name']
            phone_number = i['phone_number']
            description = i['description']

            user_list = {
                "_id": _id,
                "user_name" : user_name,
                "role" : role,
                "full_name" : full_name,
                "phone_number" : phone_number,
                "description" : description
            }

            result_list.append(user_list)
        
        return result_list
    
    def get_user_by_id(self, id):
        i = self.user_col.find_one({"_id" : ObjectId(id)})
        if i is None:
            return None
        _id = str(i['_id'])
        user_name = i['user_name']
        role = i['role']
        full_name = i['full_name']
        phone_number = i['phone_number']
        description = i['description']

        user = {
                "_id": _id,
                "user_name" : user_name,
                "role" : role,
                "full_name" : full_name,
                "phone_number" : phone_number,
                "description" : description
            }        

        return user
    

    def add_new_user(self, new_user : user):
        try:
            if (new_user.user_name.replace(" ", "").lower() == "" or
                new_user.password.replace(" ", "").lower() == "" or
                new_user.full_name == "" or
                new_user.role == "" or
                new_user.phone_number == "" or
                new_user.description == ""):
                raise ValueError('all field must not be empty')
            
            if new_user.phone_number.isdigit() == False:
                raise ValueError('phone_number input is not phone number')
            
            if self.user_col.find_one({"user_name" : new_user.user_name.replace(" ", "").lower()}) is not None:
                raise ValueError('user already exist')
    
            if self.roledb.get_role_by_name(new_user.role) is None:
                raise ValueError('role does not exist')
            
            self.user_col.insert_one({
                "user_name" : new_user.user_name.replace(" ", "").lower(),
                "password" : self.hash_util.DoHashPassword(new_user.password.replace(" ", "").lower()),
                "role" : new_user.role,
                "full_name" : new_user.full_name,
                "phone_number" : new_user.phone_number,
                "description" : new_user.description
            })

        except ValueError as e:
            raise ValueError('Error at add_new_user() : ', e)


    def update_user(self, id, update_user : user):
        try:
            if (update_user.user_name.replace(" ", "").lower() == "" or
                update_user.password.replace(" ", "").lower() == "" or
                update_user.full_name == "" or
                update_user.role == "" or
                update_user.phone_number == "" or
                update_user.description == ""):
                raise ValueError('all field must not be empty')
            
            if update_user.phone_number.isdigit() == False:
                raise ValueError('phone_number input is not phone number')
    
            if self.roledb.get_role_by_name(update_user.role) is None:
                raise ValueError('role does not exist')
            

            find_user = {"_id" : ObjectId(id)}
            updated_user = {"$set" :{
                "password" : self.hash_util.DoHashPassword(update_user.password.replace(" ", "").lower()),
                "role" : update_user.role,
                "full_name" : update_user.full_name,
                "phone_number" : update_user.phone_number,
                "description" : update_user.description
            }}

            self.user_col.update_one(find_user, updated_user)
        except ValueError as e:
            raise ValueError('Error at update_user() : ', e)