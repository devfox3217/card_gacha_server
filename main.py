import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
import auth
import gacha
from scheduler import increase_draw_counts

# 앱 시작 시 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI의 새로운 lifespan 기능을 사용하여 시작/종료 이벤트를 관리합니다.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱이 시작될 때 백그라운드에서 스케줄러 작업을 실행합니다.
    scheduler_task = asyncio.create_task(increase_draw_counts())
    
    yield # 여기에서 실제 FastAPI 애플리케이션이 동작합니다.
    
    # 서버가 종료될 때 스케줄러 작업도 안전하게 취소합니다.
    scheduler_task.cancel()

# lifespan을 FastAPI 앱에 등록합니다.
app = FastAPI(lifespan=lifespan)

# 라우터 포함
app.include_router(auth.router)
app.include_router(gacha.router)

@app.get("/")
async def root():
    return {"message": "Server is running"}
