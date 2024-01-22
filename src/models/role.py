from pydantic import BaseModel
from permission import permission


class role(BaseModel):
    role_name : str
    permissions : list