from typing import List, Dict, Any
from app.services.qwen_service import qwen_service
from app.core.logger import logger
from app.services.rag_service import rag_service

async def get_content(message: List[Dict[str, str]]) -> str:
    """基础对话内容获取函数"""
    try:
        messages = [{
            "role": "system",
            "content": "你是一个专业的出行推荐官"
        }]
        messages.extend(message)
        return await qwen_service.create_completion(messages)
    except Exception as e:
        logger.error(f"获取内容失败: {str(e)}")
        raise

async def search_spot_info(**kwargs) -> str:
    """景点信息搜索工具"""
    spot_list = kwargs.get("spot_list", [])
    summary = kwargs.get("summary", "")
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary)
    logger.info(f"RAG 增强后的 summary: {enhanced_summary}")
    
    messages = [
        {"role": "assistant", "content": enhanced_summary},
        {"role": "user", "content": f"请详细介绍以下景点的信息（包括门票价格、开放时间、交通方式等实用信息）：{spot_list}"}
    ]
    return await get_content(messages)

async def spot_recommend(**kwargs) -> str:
    """景点推荐工具"""
    summary = kwargs.get('summary', '')
    season = kwargs.get('season', '')
    days = kwargs.get('days', '')
    preference = kwargs.get('preference', '')
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary)
    logger.info(f"RAG 增强后的 summary: {enhanced_summary}")
    
    prompt = "请推荐一些值得游览的景点，"
    if season:
        prompt += f"考虑{season}季节特点，"
    if days:
        prompt += f"适合{days}天行程，"
    if preference:
        prompt += f"特别关注{preference}类型的景点，"
    prompt += "并说明推荐理由。"
    
    messages = [
        {"role": "assistant", "content": enhanced_summary},
        {"role": "user", "content": prompt}
    ]
    return await get_content(messages)

async def spot_route_recommend(**kwargs) -> str:
    """路线推荐工具"""
    summary = kwargs.get('summary', '')
    spot_name = kwargs.get("spot_name", "")
    transport = kwargs.get("transport", "")
    time_budget = kwargs.get("time_budget", "")
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary)
    logger.info(f"RAG 增强后的 summary: {enhanced_summary}")
    
    prompt = f"请为{spot_name}规划详细的游览路线，"
    if transport:
        prompt += f"使用{transport}作为主要交通工具，"
    if time_budget:
        prompt += f"游览时间预计{time_budget}，"
    prompt += "包括具体路线安排、时间分配、用餐建议等。"
    
    messages = [
        {"role": "assistant", "content": enhanced_summary},
        {"role": "user", "content": prompt}
    ]
    return await get_content(messages)

async def deep_search(**kwargs) -> str:
    """深度搜索工具"""
    summary = kwargs.get('summary', '')
    focus = kwargs.get('focus', '')
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary)
    logger.info(f"RAG 增强后的 summary: {enhanced_summary}")
    
    prompt = "请深入分析用户的旅游需求，"
    if focus:
        prompt += f"特别关注{focus}方面，"
    prompt += "提供个性化的深度游建议，包括文化体验、地道美食、特色活动等。"
    
    messages = [
        {'role': 'assistant', 'content': enhanced_summary},
        {"role": "user", "content": prompt}
    ]
    return await get_content(messages)

async def add_required_spot(**kwargs) -> str:
    """添加必选景点工具"""
    summary = kwargs.get('summary', '')
    spot_name = kwargs.get("spot_name", "")
    reason = kwargs.get("reason", "")
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary)
    logger.info(f"RAG 增强后的 summary: {enhanced_summary}")
    
    prompt = f"将{spot_name}加入必选景点列表，"
    if reason:
        prompt += f"原因是{reason}，"
    prompt += "并提供该景点的特色亮点和游览建议。"
    
    messages = [
        {'role': 'assistant', 'content': enhanced_summary},
        {"role": "user", "content": prompt}
    ]
    return await get_content(messages)

async def travel_tips(**kwargs) -> str:
    """旅行贴士工具"""
    summary = kwargs.get('summary', '')
    destination = kwargs.get('destination', '')
    aspect = kwargs.get('aspect', '')
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary)
    logger.info(f"RAG 增强后的 summary: {enhanced_summary}")
    
    prompt = f"请提供{destination}的实用旅行贴士，"
    if aspect:
        prompt += f"特别是关于{aspect}方面的建议，"
    prompt += "包括最佳旅行时间、注意事项、当地习俗等信息。"
    
    messages = [
        {'role': 'assistant', 'content': enhanced_summary},
        {"role": "user", "content": prompt}
    ]
    return await get_content(messages)

async def general_tool(**kwargs) -> str:
    """通用工具"""
    summary = kwargs.get('summary', '')
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary)
    logger.info(f"RAG 增强后的 summary: {enhanced_summary}")
    
    messages = [
        {'role': 'assistant', 'content': enhanced_summary},
        {"role": "user", "content": "根据上文回答问题并给出通用解答"}
    ]
    return await get_content(messages)

# 工具函数映射表
tool_funcs = {
    "general_tool": general_tool,
    "search_spot_info": search_spot_info,
    "spot_recommend": spot_recommend,
    "spot_route_recommend": spot_route_recommend,
    "deep_search": deep_search,
    "add_required_spot": add_required_spot,
    "travel_tips": travel_tips
} 