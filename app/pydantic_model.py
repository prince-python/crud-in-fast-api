from pydantic import BaseModel

class Person(BaseModel):
    name:str
    phone:int
    email:str
    password:str
    
    
    
    
    
    
class Loginuser(BaseModel):
    email:str
    password:str
    
class Token (BaseModel):
    access_token: str
    token_type: str= 'bearer'
    
    
    
    
class Delete(BaseModel):
    id:int

class Get_Person(BaseModel):
    id:int

class Update_Person(BaseModel):
    id:int
    email:str
    name:str
    phone:str
    password:str