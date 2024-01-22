import sys
sys.path.append('./src/schemas')
sys.path.append('./src/models')

from response_obj import response_obj
from user import user
from permission import permission
from role import role
from role_schema import role_schema
from permission_schema import permission_schema
from user_schema import user_schema
from permission_schema import permission_schema
from fastapi import FastAPI

app = FastAPI()


#-------------------------------------------------------------------API for Users (/api/user)
#--------Start CRUD---------

@app.get("/api/user/lists")
async def get_list_of_user():
    db = user_schema()
    return response_obj(status="SUCCESS", message="get user list", object=db.get_user_list())


@app.get("/api/user/{id}")
async def get_user_by_id(id : str):
    db = user_schema()
    found_user = db.get_user_by_id(id)

    if found_user is not None:
        return response_obj(status="SUCCESS", message="found user !", object=found_user)
    else:
        return response_obj(status="FAILED", message="user not found !", object=found_user)
    
@app.post("/api/user/add")
async def add_user(new_user : user):
    try:
        db = user_schema()
        db.add_new_user(new_user=new_user)

        return response_obj(status="SUCCESS", message="Added user successfully !", object=new_user)

    except ValueError as e:
        return response_obj(status="FAILED", message="error: "+str(e), object=None)
    
@app.put("/api/user/{id}")
async def update_user(id : str, update_user : user):
    try:
        db = user_schema()
        db.update_user(id, update_user)
        return response_obj(status="SUCCESS", message="updated user:", object=update_user)
    except ValueError as e:
        return response_obj(status="FAILED", message="error: "+str(e), object=None)
    

#--------End CRUD------------
    

#----------------start optional function--------------------
#----------------end optional function----------------------
    


#-------------------------------------------------------------------API for Roles (/api/role)
#--------Start CRUD---------
@app.get("/api/role/list")
async def get_list_of_role():
    db = role_schema()
    return response_obj(status="SUCCESS", message="get role list", object=db.get_per_list())

@app.get("/api/role/{id}")
async def get_role_by_id(id : str):
    db = role_schema()
    result = db.get_role_by_id(id)
    if result is not None:
        return response_obj(status="SUCCESS", message="found role", object=result)
    
    else:
        return response_obj(status="FAILED", message="role not found", object=None)
    
@app.post("/api/role/add")
async def add_role(new_role : role):
    try:
        db = role_schema()
        db.add_new_role(new_role)
        return response_obj(status="SUCCESS", message="added role", object=new_role)
    except ValueError as e:
        return response_obj(status="FAILED", message="error:" + str(e), object=None)
    
@app.put("/api/role/{id}")
async def update_role(id : str, updated_role : role):
    try:
        db = role_schema()
        db.update_role(id, updated_role)
        return response_obj(status="SUCCESS", message="updated role", object=updated_role)
    except ValueError as e:
        return response_obj(status="FAILED", message="error:" + str(e), object=None)  


#--------End CRUD-----------
#-------------------------------------------------------------------API for permission (/api/permission)
#--------Start CRUD---------
@app.get("/api/permission/lists")
async def get_list_of_permission():
    db = permission_schema()
    return response_obj(status="SUCCESS", message="get permission list", object=db.get_per_list())

@app.post("/api/permission/add")
async def add_permission(new_permission : permission):
    try:
        db = permission_schema()
        db.add_new_per(new_permission)
        return response_obj(status="SUCCESS", message="added permission successfully", object=new_permission)      
    except ValueError as e:
        return response_obj(status="FAILED", message="ERROR: "+str(e), object=None)

#--------End CRUD-----------