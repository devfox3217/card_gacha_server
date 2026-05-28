import json
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Session
from database import Base, get_db
from auth import get_current_user, UserDB, get_user

# 가챠(뽑기) 기능을 위한 라우터
router = APIRouter(prefix="/gacha", tags=["gacha"])

# 인벤토리 데이터베이스 모델
class InventoryDB(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    card_number = Column(Integer, index=True)
    quantity = Column(Integer, default=0)

# 서버 시작 시 JSON 파일에서 카드 데이터 로드
with open("cards.json", "r", encoding="utf-8") as f:
    CARDS_DATA = json.load(f)

# 빠른 등급 검색을 위한 딕셔너리 생성
CARD_RANK_MAP = {card["number"]: card["rank"] for card in CARDS_DATA}

# 뽑기 확률을 위해 random 가중치만 추출한 리스트
CARD_WEIGHTS = [card["random"] for card in CARDS_DATA]

@router.post("/draw")
def draw_card(times: int = 1, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    """
    지정된 횟수(times)만큼 카드를 뽑고 사용자의 인벤토리에 저장합니다. 기본 1회.
    """
    # 가중치 기반으로 카드 뽑기 수행
    drawn_cards = random.choices(CARDS_DATA, weights=CARD_WEIGHTS, k=times)
    
    # 뽑은 카드를 DB에 저장 (동일한 카드를 여러장 뽑을 경우 최적화를 위해 메모리 합산)
    drawn_summary = {}
    for card in drawn_cards:
        num = card["number"]
        drawn_summary[num] = drawn_summary.get(num, 0) + 1
        
    for card_number, quantity in drawn_summary.items():
        # 사용자의 인벤토리에 해당 카드가 이미 있는지 확인하는 분기
        inventory_item = db.query(InventoryDB).filter(
            InventoryDB.user_id == current_user.id,
            InventoryDB.card_number == card_number
        ).first()
        
        # 카드가 있으면 수량만 증가시키고, 없으면 새로 추가하는 분기
        if inventory_item:
            inventory_item.quantity += quantity
        else:
            new_item = InventoryDB(
                user_id=current_user.id,
                card_number=card_number,
                quantity=quantity
            )
            db.add(new_item)
            
    db.commit()
    
    return {
        "message": f"{times}장의 카드를 뽑았습니다!",
        "drawn_cards": drawn_cards
    }

@router.get("/inventory")
def get_inventory(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    """
    현재 사용자가 보유한 모든 카드의 종류와 수량을 반환합니다.
    """
    # DB에서 현재 사용자의 모든 인벤토리 기록 조회
    inventory_items = db.query(InventoryDB).filter(InventoryDB.user_id == current_user.id).all()
    
    result = []
    for item in inventory_items:
        # 번호에 해당하는 카드 상세 정보 매칭
        card_info = next((c for c in CARDS_DATA if c["number"] == item.card_number), None)
        if card_info:
            result.append({
                "card": card_info,
                "quantity": item.quantity
            })
            
    # 반환 시 보기 좋게 카드 번호순으로 정렬
    result.sort(key=lambda x: x["card"]["number"])
    return {"inventory": result}

def calculate_inventory_score(db: Session, user_id: int):
    """
    특정 사용자의 인벤토리 점수를 계산하는 유틸리티 함수.
    등급별로 카드를 몇 종류 가지고 있는지 합산합니다.
    (예: N등급 3종류, R등급 2종류 -> score: {"N": 3, "R": 2})
    """
    inventory_items = db.query(InventoryDB).filter(InventoryDB.user_id == user_id).all()
    
    # 등급별 보유 카드 '종류' 수를 저장할 딕셔너리 초기화
    score = {"SSSR": 0, "SSR": 0, "SR": 0, "R": 0, "N": 0}
    
    for item in inventory_items:
        # 수량이 1개 이상인 카드만 계산에 포함
        if item.quantity > 0:
            rank = CARD_RANK_MAP.get(item.card_number)
            if rank in score:
                score[rank] += 1
                
    return score

@router.get("/compare/{other_username}")
def compare_inventory(other_username: str, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    """
    현재 사용자와 다른 사용자의 카드 보유 상황(각 등급별 카드 종류의 수)을 비교합니다.
    """
    # 비교 대상 사용자가 DB에 존재하는지 확인
    target_user = get_user(db, other_username)
    
    # 사용자가 없으면 null (FastAPI에서는 None) 반환
    if not target_user:
        return None
        
    # 점수 계산
    my_score = calculate_inventory_score(db, current_user.id)
    target_score = calculate_inventory_score(db, target_user.id)
    
    return {
        "my_username": current_user.username,
        "my_score": my_score,
        "target_username": target_user.username,
        "target_score": target_score
    }
