from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class FunctionType(str, Enum):
    SEARCH_SPOT = "search_spot_info"
    ROUTE_PLAN = "spot_route_info"
    DEEP_SEARCH = "deep_search"
    ADD_SPOT = "add_required_spot"
    GENERAL_TOOL = "general_tool"

class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class BaseResponse(BaseModel):
    status: ResponseStatus
    message: str
    data: Optional[Any] = None

class SpotInfo(BaseModel):
    """景点信息模型"""
    name: str
    description: str
    location: str
    images: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    rating: Optional[float] = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "images": self.images,
            "tags": self.tags,
            "rating": self.rating
        }

class RouteInfo(BaseModel):
    """路线信息模型"""
    spots: List[str]
    order: List[int]
    duration: str
    description: str
    transportation: Optional[str] = "步行"
    estimated_cost: Optional[float] = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "spots": self.spots,
            "order": self.order,
            "duration": self.duration,
            "description": self.description,
            "transportation": self.transportation,
            "estimated_cost": self.estimated_cost
        }

class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str
    content: str
    timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        } 