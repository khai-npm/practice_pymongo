from pydantic import BaseModel


class response_obj(BaseModel):
    status : str
    message : str
    object : object