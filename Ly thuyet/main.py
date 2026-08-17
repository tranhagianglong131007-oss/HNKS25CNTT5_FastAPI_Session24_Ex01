from fastapi import FastAPI , Request
from database import Base , engine
import models
from fastapi.middleware.cors import CORSMiddleware
import time
from routers.auth_router import auth_router
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router=auth_router)

# CORS : Các HTTP được chấp nhận có thể gưi phản hồi 
list_allow = [
    "http://127.0.0.1:3000/",
    "http://127.0.0.1:3001/",
    "http://127.0.0.1:3002/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=list_allow,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# middleware : Bản chất nó là một hàm hoặc một class dùng để chạy tự động cho mọi request mà nó nhận về 
# Nhiệm vụ : dùng có các tác vụ - đo thời gian của một api , ghi log , xác thực người dùng , hoặc là nén , kiểm tra dữ liệu 

@app.middleware("http")
async def handle_calc_time_api (request : Request , call_next):
    start_time = time.time()

    response = await call_next(request)

    end_time = time.time() - start_time 
    print(end_time)
    return response

