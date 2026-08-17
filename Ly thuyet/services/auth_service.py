from schemals.auth_schemal import LoginResponse , RegisterResponse , RegisterAccountRequest , LoginRequest
from sqlalchemy.orm import Session
from models import UserModel
from utils import security
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from fastapi import Depends , HTTPException
import jwt 

FOUND_USER = "Tên Tài Khoản Đã Tồn Tại"
FOUND_EMAIL = "Email đã tồn tại"
NOT_FOUND_USER = "Không tìm thấy tên người dùng"
NOT_CORRECT_PASSWORD = "Mật Khẩu Sai"
EXPIRED_SIGNATURE_ERROR = "Hết hạn token"

def handle_register_service (user_account : RegisterAccountRequest , db : Session) : 
    user = db.query(UserModel).filter(UserModel.username == user_account.username).first()
    if user: 
        return FOUND_USER

    email = db.query(UserModel).filter(UserModel.email == user_account.email).first()
    if email:
        return FOUND_EMAIL
    hash_password = security.handle_hash_password(user_account.password)

    new_account = UserModel(
        username = user_account.username ,
        password = hash_password , 
        email = user_account.email, 
        role_id = 3
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

def handle_login_service (user_account : LoginRequest , db : Session) : 
    user = db.query(UserModel).filter(UserModel.username == user_account.username).first()

    if not user: 
        return NOT_FOUND_USER

    is_account_user = security.check_password(user_account.password , user.password)

    if not is_account_user: 
        return NOT_CORRECT_PASSWORD

    access_token = security.create_access_token(user.id , user.username ,user.role.role_name)

    return access_token

security_token = HTTPBearer()
def handle_get_user (credentials : HTTPAuthorizationCredentials = Depends(security_token)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token,security.SECRET_KEY, security.ALG)
        print(f"payload : {payload}")
        user_name = payload.get("user_name")
        role_name = payload.get("role_account")
        user_id = payload.get("sup")
        data = {
            "username" : user_name,
            "role_name" : role_name,
            "user_id" : user_id
        }
        return data
    except jwt.ExpiredSignatureError:
        return EXPIRED_SIGNATURE_ERROR

# Tạo một lớp phân quyền 
class RoleCheck : 
    def __init__(self,allow_roles : list):
        self.allow_roles = allow_roles

    def __call__(self, user_data : dict = Depends(handle_get_user)): # sử dụng checkroll sẽ tự động gọi call
        user_role_name = user_data.get("role_name")
        print(f"user_role_name:{user_role_name}")
        if user_role_name not in self.allow_roles :
            raise HTTPException(
                status_code=403 ,
                detail=f"Quyền {user_role_name} không được thực hiện hành động này"
            )
        return user_data