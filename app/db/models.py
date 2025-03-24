from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime, UTC

class Spot(Base):
    """景点数据模型"""
    __tablename__ = "spots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    images = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "images": self.images,
            "tags": self.tags,
            "rating": self.rating
        }

class Route(Base):
    """路线数据模型"""
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    spots = Column(JSON)  # 存储景点ID列表
    order = Column(JSON)  # 存储景点访问顺序
    duration = Column(String)
    description = Column(String)
    transportation = Column(String, default="步行")
    estimated_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    def to_dict(self):
        return {
            "id": self.id,
            "spots": self.spots,
            "order": self.order,
            "duration": self.duration,
            "description": self.description,
            "transportation": self.transportation,
            "estimated_cost": self.estimated_cost
        }

class ChatHistory(Base):
    """聊天历史数据模型"""
    __tablename__ = "chat_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    content = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))
    
    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        } 