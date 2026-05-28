import asyncio
from sqlalchemy.orm import Session
from database import SessionLocal
from auth import UserDB

# 사용자의 뽑기 횟수를 1씩 증가시키는 함수 (최대 30)
async def increase_draw_counts():
    while True:
        # 10분(600초) 대기
        await asyncio.sleep(600)
        
        # 데이터베이스 세션 생성
        db: Session = SessionLocal()
        try:
            # 모든 사용자 조회
            users = db.query(UserDB).all()
            for user in users:
                # 최대 횟수 30개 제한 분기
                if user.draw_count < 30:
                    user.draw_count += 1
            
            # 변경 사항 커밋
            db.commit()
            print("모든 사용자의 뽑기 횟수가 1씩 증가했습니다. (최대 30)")
        except Exception as e:
            print(f"뽑기 횟수 증가 중 오류 발생: {e}")
        finally:
            # 세션 닫기
            db.close()
