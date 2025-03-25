from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from app.db.base import Base
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")

class Spot(Base):
    """景点"""
    __tablename__ = "spots"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)  # 景点名称
    description = Column(Text)  # 景点描述
    location = Column(String)  # 位置
    images = Column(JSON)  # 图片URL列表
    tags = Column(JSON)  # 标签列表
    rating = Column(Float)  # 评分
    vector_embedding = Column(JSON)  # 向量嵌入
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "images": self.images,
            "tags": self.tags,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class Route(Base):
    """路线"""
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)  # 路线名称
    description = Column(Text)  # 路线描述
    spots = Column(JSON)  # 景点列表
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "spots": self.spots,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class ChatHistory(Base):
    """聊天历史"""
    __tablename__ = "chat_histories"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String)  # 会话ID
    user_query = Column(Text)  # 用户查询
    assistant_response = Column(Text)  # 助手回复
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_query": self.user_query,
            "assistant_response": self.assistant_response,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class VectorIndex(Base):
    """向量索引"""
    __tablename__ = "vector_indices"
    
    id = Column(Integer, primary_key=True)
    collection_name = Column(String)  # spots, routes, chat_histories 等
    record_id = Column(Integer)  # 对应记录的ID
    vector = Column(JSON)  # 向量数据
    meta_info = Column(JSON)  # 额外元数据
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "collection_name": self.collection_name,
            "record_id": self.record_id,
            "meta_info": self.meta_info,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        } 