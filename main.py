from fastapi import FastAPI
from database import engine, Base
import auth
import gacha

# 앱 시작 시 데이터베이스 테이블 생성
# Base에 등록된 모든 모델(auth의 UserDB, gacha의 InventoryDB)의 테이블을 생성합니다.
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 라우터 포함
app.include_router(auth.router)
app.include_router(gacha.router)

@app.get("/")
async def root():
    return {"message": "Server is running"}
