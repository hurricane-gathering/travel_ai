from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import Spot, Route
from app.utils import tool_function
from app.core.logger import logger
from app.services.vector_store import vector_store
from app.services.rag_service import rag_service

@tool_function
async def search_similar_spots(query: str, top_k: int = 5) -> List[Dict]:
    """
    搜索相似的景点
    
    Args:
        query: 搜索查询文本
        top_k: 返回结果数量
        
    Returns:
        List[Dict]: 相似景点列表
    """
    try:
        logger.info(f"开始搜索相似景点: query={query}, top_k={top_k}")
        
        # 使用 RAG 增强查询
        enhanced_query = await rag_service.enhance_query(query)
        logger.info(f"RAG 增强后的查询: {enhanced_query}")
        
        # 执行向量搜索
        results = vector_store.search("spots", enhanced_query, k=top_k)
        logger.info(f"向量搜索返回 {len(results)} 个结果")
        
        # 获取景点详细信息
        spot_ids = [r["record_id"] for r in results]
        with Session() as session:
            spots = session.query(Spot).filter(Spot.id.in_(spot_ids)).all()
            spot_map = {s.id: s for s in spots}
            logger.info(f"从数据库获取到 {len(spots)} 个景点详情")
            
        # 组装返回结果
        enriched_results = []
        for result in results:
            spot = spot_map.get(result["record_id"])
            if spot:
                enriched_results.append({
                    "id": spot.id,
                    "name": spot.name,
                    "description": spot.description,
                    "location": spot.location,
                    "score": 1.0 / (1.0 + result["distance"])  # 将距离转换为相似度分数
                })
                
        logger.info(f"搜索完成，返回 {len(enriched_results)} 个景点")
        return enriched_results
        
    except Exception as e:
        logger.error(f"搜索相似景点失败: {str(e)}")
        raise

@tool_function
async def search_similar_routes(query: str, top_k: int = 5) -> List[Dict]:
    """
    搜索相似的路线
    
    Args:
        query: 搜索查询文本
        top_k: 返回结果数量
        
    Returns:
        List[Dict]: 相似路线列表
    """
    try:
        logger.info(f"开始搜索相似路线: query={query}, top_k={top_k}")
        
        # 使用 RAG 增强查询
        enhanced_query = await rag_service.enhance_query(query)
        logger.info(f"RAG 增强后的查询: {enhanced_query}")
        
        # 执行向量搜索
        results = vector_store.search("routes", enhanced_query, k=top_k)
        logger.info(f"向量搜索返回 {len(results)} 个结果")
        
        # 获取路线详细信息
        route_ids = [r["record_id"] for r in results]
        with Session() as session:
            routes = session.query(Route).filter(Route.id.in_(route_ids)).all()
            route_map = {r.id: r for r in routes}
            logger.info(f"从数据库获取到 {len(routes)} 个路线详情")
            
        # 组装返回结果
        enriched_results = []
        for result in results:
            route = route_map.get(result["record_id"])
            if route:
                enriched_results.append({
                    "id": route.id,
                    "name": route.name,
                    "description": route.description,
                    "spots": route.spots,
                    "score": 1.0 / (1.0 + result["distance"])  # 将距离转换为相似度分数
                })
                
        logger.info(f"搜索完成，返回 {len(enriched_results)} 个路线")
        return enriched_results
        
    except Exception as e:
        logger.error(f"搜索相似路线失败: {str(e)}")
        raise 