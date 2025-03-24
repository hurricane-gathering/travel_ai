from sqlalchemy.orm import Session
from app.models.base import SpotInfo, RouteInfo
from app.db.models import Spot, Route
from typing import List, Optional

def create_spot(db: Session, spot: SpotInfo) -> Spot:
    """创建新景点"""
    db_spot = Spot(
        name=spot.name,
        description=spot.description,
        location=spot.location,
        images=spot.images,
        tags=spot.tags,
        rating=spot.rating
    )
    db.add(db_spot)
    db.commit()
    db.refresh(db_spot)
    return db_spot

def get_spots(db: Session, query: str, skip: int = 0, limit: int = 10) -> List[Spot]:
    """搜索景点"""
    return db.query(Spot).filter(
        Spot.name.ilike(f"%{query}%") |
        Spot.description.ilike(f"%{query}%") |
        Spot.tags.any(query)
    ).offset(skip).limit(limit).all()

def create_route(db: Session, route: RouteInfo) -> Route:
    """创建新路线"""
    db_route = Route(
        spots=route.spots,
        order=route.order,
        duration=route.duration,
        description=route.description,
        transportation=route.transportation,
        estimated_cost=route.estimated_cost
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

def get_route(db: Session, route_id: int) -> Optional[Route]:
    """获取路线"""
    return db.query(Route).filter(Route.id == route_id).first()

def update_spot(db: Session, spot_id: int, spot: SpotInfo) -> Optional[Spot]:
    """更新景点信息"""
    db_spot = db.query(Spot).filter(Spot.id == spot_id).first()
    if db_spot:
        for key, value in spot.dict(exclude_unset=True).items():
            setattr(db_spot, key, value)
        db.commit()
        db.refresh(db_spot)
    return db_spot

def delete_spot(db: Session, spot_id: int) -> bool:
    """删除景点"""
    db_spot = db.query(Spot).filter(Spot.id == spot_id).first()
    if db_spot:
        db.delete(db_spot)
        db.commit()
        return True
    return False 