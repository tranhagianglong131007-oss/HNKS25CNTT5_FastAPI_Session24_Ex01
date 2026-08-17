from fastapi import APIRouter , status , Depends
from schemals.auth_schemal import LoginResponse , RegisterResponse , RegisterAccountRequest , LoginRequest, InfoUserResponse
from sqlalchemy.orm import Session
from database import get_db
from services import auth_service

#  Tạo bộ định tuyền 

auth_router = APIRouter(prefix="/auth" , tags=["Authentications"])


@auth_router.post("/login",response_model=LoginResponse,status_code=status.HTTP_200_OK)
def handle_login(login_data : LoginRequest , db : Session = Depends(get_db)) :
    data_response = auth_service.handle_login_service(user_account=login_data,db=db)
    return {"message" : "Đăng nhập thành công" , "access_token" : data_response , "token_type" : "bearer"}

@auth_router.post("/register",response_model=RegisterResponse ,status_code=status.HTTP_201_CREATED)
def handle_register_account (user_account : RegisterAccountRequest , db : Session = Depends(get_db)) : 
    data_response = auth_service.handle_register_service(user_account=user_account,db=db)

    if data_response != "Tên Tài Khoản Đã Tồn Tại":
        return {"message" : "Đăng ký tài khoản thành công" , "username" : data_response.username} 
    return {"message":"Đăng ký thất bại", "username":None}

@auth_router.post("/get_info_user",response_model=InfoUserResponse,status_code=status.HTTP_200_OK)
def handle_get_info_user (user_info : dict = Depends(auth_service.handle_get_user)): 
    return {"message" : "Lấy dữ liệu thành công" , "data" : user_info}


@auth_router.get("/get_data" ,dependencies=[Depends(auth_service.RoleCheck(["Admin"]))])
def handle_get_all_data ():
    return {"message" : "Lấy danh sách toàn bộ dự án"}