from pydantic import BaseModel

class LoginResponse(BaseModel): 
    access_token : str
    token_type : str 
    message : str

class RegisterResponse(BaseModel): 
    message : str 
    username : str | None

class RegisterAccountRequest(BaseModel) : 
    username : str 
    password : str 
    email : str

class LoginRequest(BaseModel):
    username : str
    password : str 

class InfoUser(BaseModel):
    username : str
    user_id : int
    role_name : str 

class InfoUserResponse(BaseModel):
    message : str
    data : InfoUser