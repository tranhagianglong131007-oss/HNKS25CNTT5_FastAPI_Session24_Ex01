import bcrypt 
import jwt

from datetime import datetime , timedelta , timezone 

SECRET_KEY = "longtran123"
ALG = "HS256"

def handle_hash_password (raw_password : str) -> str : 
    return bcrypt.hashpw(raw_password.encode(),bcrypt.gensalt())


def check_password (raw_password : str , hash_password : str) -> bool:
    return bcrypt.checkpw(raw_password.encode(),hash_password.encode())


def create_access_token(user_id : int , username : str  ,role_user : str) -> str:
    time = datetime.now(timezone.utc)

    payload = {
        "sup" : user_id,
        "user_name" : username,
        "role_account" : role_user,
        "iat" : time ,
        "exp" : time + timedelta(minutes=15)
    }

    return jwt.encode(payload,SECRET_KEY,ALG)
