import asyncio
from app.services.vector_store import vector_store
from app.db.session import Session
from app.db.models import Spot, Route
from app.core.logger import logger

async def init_vector_store():
    """初始化向量数据库"""
    try:
        # 1. 从数据库获取所有景点和路线
        with Session() as session:
            spots = session.query(Spot).all()
            routes = session.query(Route).all()
            
            logger.info(f"获取到 {len(spots)} 个景点和 {len(routes)} 个路线")
            
            # 2. 构建景点文档
            for spot in spots:
                # 在 Session 上下文中获取所有需要的属性
                spot_data = {
                    "id": spot.id,
                    "name": spot.name,
                    "description": spot.description,
                    "location": spot.location,
                    "tags": spot.tags,
                    "rating": spot.rating
                }
                
                content = f"""
景点名称：{spot_data['name']}
描述：{spot_data['description']}
位置：{spot_data['location']}
标签：{', '.join(spot_data['tags']) if spot_data['tags'] else '无'}
评分：{spot_data['rating'] if spot_data['rating'] else '暂无评分'}
                """.strip()
                
                metadata = {
                    "type": "spot",
                    "name": spot_data["name"],
                    "location": spot_data["location"],
                    "tags": spot_data["tags"],
                    "rating": spot_data["rating"]
                }
                
                vector_store.add_to_index("spots", spot_data["id"], content, metadata)
                logger.info(f"添加景点到向量数据库: {spot_data['name']}")
                
            # 3. 构建路线文档
            for route in routes:
                # 在 Session 上下文中获取所有需要的属性
                route_data = {
                    "id": route.id,
                    "name": route.name,
                    "description": route.description,
                    "spots": route.spots
                }
                
                content = f"""
路线名称：{route_data['name']}
描述：{route_data['description']}
包含景点：{', '.join(route_data['spots']) if route_data['spots'] else '暂无景点'}
                """.strip()
                
                metadata = {
                    "type": "route",
                    "name": route_data["name"],
                    "spots": route_data["spots"]
                }
                
                vector_store.add_to_index("routes", route_data["id"], content, metadata)
                logger.info(f"添加路线到向量数据库: {route_data['name']}")
            
        logger.info("向量数据库初始化完成")
        
    except Exception as e:
        logger.error(f"向量数据库初始化失败: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(init_vector_store()) 