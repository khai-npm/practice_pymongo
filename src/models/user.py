from pydantic import BaseModel

class user(BaseModel):
    user_name : str
    password : str
    role : str
    full_name : str
    phone_number : str
    description : str