from typing import List, Dict, Any, Tuple
from app.services.qwen_service import qwen_service
from app.core.logger import logger
from app.services.rag_service import rag_service

async def need_followup(result: str, **kwargs) -> Tuple[bool, str]:
    """判断是否需要追问
    
    Args:
        result: 当前回答
        **kwargs: 工具特定参数
        
    Returns:
        (need_followup, followup_question): 是否需要追问及追问内容
    """
    try:
        # 构建追问判断提示词
        prompt = f"""请判断以下回答是否完整满足用户需求，如果不满足，请给出追问内容。

当前回答：
{result}

原始需求：
{kwargs.get('summary', '')}

请按以下格式返回：
需要追问：是/否
追问内容：具体的追问内容（如果需要）
"""
        
        messages = [
            {"role": "system", "content": "你是一个专业的旅游咨询质量检查员，负责判断回答是否完整满足用户需求。"},
            {"role": "user", "content": prompt}
        ]
        
        response = await qwen_service.create_completion(messages)
        
        # 解析响应
        lines = response.strip().split('\n')
        need_followup = "是" in lines[0]
        followup_question = lines[1].replace("追问内容：", "").strip() if need_followup else ""
        
        return need_followup, followup_question
        
    except Exception as e:
        logger.error(f"判断追问失败: {str(e)}")
        return False, ""

async def get_content(message: List[Dict[str, str]], **kwargs) -> str:
    """基础对话内容获取函数"""
    try:
        messages = [{
            "role": "system",
            "content": "你是一个专业的出行推荐官"
        }]
        messages.extend(message)
        
        # 获取初始回答
        result = await qwen_service.create_completion(messages)
        
        # 判断是否需要追问
        need_more, followup = await need_followup(result, **kwargs)
        logger.info(f"need_more: {need_more}, followup: {followup}")
        # 如果需要追问，将追问内容添加到对话历史
        while need_more and followup:
            messages.extend([
                {"role": "assistant", "content": result},
                {"role": "user", "content": followup}
            ])
                        
            # 获取新的回答
            result = await qwen_service.create_completion(messages)
            
            # 继续判断是否需要追问
            need_more, followup = await need_followup(result, **kwargs)
            
        return result
        
    except Exception as e:
        logger.error(f"获取内容失败: {str(e)}")
        raise

async def search_spot_info(**kwargs) -> str:
    """景点信息搜索工具"""
    spot_list = kwargs.get("spot_list", [])
    summary = kwargs.get("summary", "")
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary, "search_spot_info", spot_list=spot_list)
    
    messages = [
        {"role": "assistant", "content": enhanced_summary},
        {"role": "user", "content": f"请详细介绍以下景点的信息（包括门票价格、开放时间、交通方式等实用信息）：{spot_list}"}
    ]
    return await get_content(messages, summary=summary)

async def spot_recommend(**kwargs) -> str:
    """景点推荐工具"""
    summary = kwargs.get('summary', '')
    season = kwargs.get('season', '')
    days = kwargs.get('days', '')
    preference = kwargs.get('preference', '')
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary, "spot_recommend", 
                                                     season=season, days=days, preference=preference)
    
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
    return await get_content(messages, summary=summary)

async def spot_route_recommend(**kwargs) -> str:
    """路线推荐工具"""
    summary = kwargs.get('summary', '')
    spot_name = kwargs.get("spot_name", "")
    transport = kwargs.get("transport", "")
    time_budget = kwargs.get("time_budget", "")
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary, "spot_route_recommend",
                                                     spot_name=spot_name, transport=transport, time_budget=time_budget)
    
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
    return await get_content(messages, summary=summary)

async def deep_search(**kwargs) -> str:
    """深度搜索工具"""
    summary = kwargs.get('summary', '')
    focus = kwargs.get('focus', '')
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary, "deep_search", focus=focus)
    
    prompt = "请深入分析用户的旅游需求，"
    if focus:
        prompt += f"特别关注{focus}方面，"
    prompt += "提供个性化的深度游建议，包括文化体验、地道美食、特色活动等。"
    
    messages = [
        {'role': 'assistant', 'content': enhanced_summary},
        {"role": "user", "content": prompt}
    ]
    return await get_content(messages, summary=summary)

async def add_required_spot(**kwargs) -> str:
    """添加必选景点工具"""
    summary = kwargs.get('summary', '')
    spot_name = kwargs.get("spot_name", "")
    reason = kwargs.get("reason", "")
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary, "general_tool")
    
    prompt = f"将{spot_name}加入必选景点列表，"
    if reason:
        prompt += f"原因是{reason}，"
    prompt += "并提供该景点的特色亮点和游览建议。"
    
    messages = [
        {'role': 'assistant', 'content': enhanced_summary},
        {"role": "user", "content": prompt}
    ]
    return await get_content(messages, summary=summary)

async def travel_tips(**kwargs) -> str:
    """旅行贴士工具"""
    summary = kwargs.get('summary', '')
    destination = kwargs.get('destination', '')
    aspect = kwargs.get('aspect', '')
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary, "general_tool")
    
    prompt = f"请提供{destination}的实用旅行贴士，"
    if aspect:
        prompt += f"特别是关于{aspect}方面的建议，"
    prompt += "包括最佳旅行时间、注意事项、当地习俗等信息。"
    
    messages = [
        {'role': 'assistant', 'content': enhanced_summary},
        {"role": "user", "content": prompt}
    ]
    return await get_content(messages, summary=summary)

async def general_tool(**kwargs) -> str:
    """通用工具"""
    summary = kwargs.get('summary', '')
    
    # 使用 RAG 服务处理 summary
    enhanced_summary = await rag_service.enhance_query(summary, "general_tool")
    
    messages = [
        {'role': 'assistant', 'content': enhanced_summary},
        {"role": "user", "content": "根据上文回答问题并给出通用解答"}
    ]
    return await get_content(messages, summary=summary)

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