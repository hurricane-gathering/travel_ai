from fastapi import APIRouter, HTTPException
from app.models.base import ResponseStatus, BaseResponse
from app.services.qwen_service import qwen_service
from app.services.executor import execute_tool
from app.core.logger import logger
from app.core.tools import tool_desc
from typing import List, Dict, Any
import json

api_router = APIRouter()

# 对话历史记录
histories = [{
    "role": "system",
    "content": "你是一个专业的出行推荐官"
}]

def print_chat_history():
    """打印当前对话历史"""
    logger.info("\n=== 当前对话历史 ===")
    for idx, msg in enumerate(histories):
        role = msg["role"]
        content = msg["content"]
        # 为不同角色设置不同的前缀
        prefix = "🤖" if role == "assistant" else "👤" if role == "user" else "🌟"
        logger.info(f"{prefix} {role}: {content}")
    logger.info("==================\n")

async def optimization(messages: list) -> str:
    """多轮对话内容总结优化"""
    if not messages or len(messages) < 2:
        return ""
        
    system_messages = [{
        "role": "system",
        "content": "你是一个专业的大模型改写优化家,总结下面的多轮对话内容"
    }]
    system_messages.extend(messages)
    
    try:
        response = await qwen_service.create_completion(system_messages)
        return response
    except Exception as e:
        logger.error(f"对话优化失败: {str(e)}")
        return ""

def generate_prompt(query: str) -> str:
    return f"""
解析用户意图: {query}

你是一位资深旅行规划师，请根据用户输入及上下文，严格按以下规则输出JSON格式的功能调用：

### 可用工具列表：
{tool_desc}

### 强制规则：
1. 必须按照以下JSON格式输出，不要添加其他描述：
{{
  "actionType": "singleFunction" 或 "multiFunction", // 单功能或多功能调用
  "functions": [
    {{
      "funcName": "工具名称",
      "parameters": [
        {{ "name": "参数名1", "value": "参数值1" }},
        {{ "name": "参数名2", "value": "参数值2" }}
      ]
    }},
    ...更多功能 (仅当actionType为multiFunction时)
  ]
}}

2. 工具名称必须从可用工具列表中选择，禁止编造新工具
3. 参数需从输入中直接抽取，禁止自行生成或假设值
4. 如果需要多工具协作处理，将actionType设为"multiFunction"并按顺序添加多个功能
5. 如果无法匹配具体工具，使用"general_tool"作为通用工具

### 工具调用规则：
1. 景点搜索工具(search_spots)：
   - 用于搜索特定景点信息
   - 参数：query（搜索关键词）
   - 返回：景点基本信息列表

2. 路线规划工具(plan_route)：
   - 用于规划多个景点的游览路线
   - 参数：spots（景点列表）
   - 返回：优化后的游览路线

3. 景点添加工具(add_spot)：
   - 用于添加新的景点信息
   - 参数：name（景点名称）、description（描述）、location（位置）
   - 返回：添加成功的景点信息

4. 通用工具(general_tool)：
   - 用于处理无法匹配到具体工具的情况
   - 参数：query（用户查询内容）
   - 返回：通用回复信息

### 多工具协作示例：
当用户需要"帮我规划北京故宫和长城的游览路线"时，应该：
1. 先使用search_spots工具分别搜索故宫和长城的信息
2. 然后使用plan_route工具规划这两个景点的游览路线
3. actionType应设置为"multiFunction"
4. functions数组中应包含这两个工具的调用信息
"""

@api_router.post("/chat", response_model=BaseResponse)
async def chat_endpoint(query: str):
    """
    处理用户查询
    """
    try:
        # 1. 添加用户消息到历史记录
        histories.append({"role": "user", "content": query})
        print_chat_history()  # 打印添加用户消息后的历史
        
        # 2. 优化多轮对话内容
        optimized_content = await optimization(histories[-5:])  # 只取最近5轮对话进行优化
        
        # 3. 生成提示词
        prompt = generate_prompt(query)
        
        # 4. 调用模型解析意图，使用优化后的对话内容
        messages = [{
            "role": "system",
            "content": "你是一个专业的出行推荐官"
        }]
        if optimized_content:
            messages.append({
                "role": "assistant",
                "content": optimized_content
            })
        messages.append({"role": "user", "content": prompt})
        response = await qwen_service.create_completion(messages)
        
        # 5. 执行工具调用
        result = await execute_tool(response, optimized_content, query)
        
        # 6. 添加助手回复到历史记录
        histories.append({"role": "assistant", "content": result})
        print_chat_history()  # 打印添加助手回复后的历史
        
        # 7. 返回结果
        return BaseResponse(
            status=ResponseStatus.SUCCESS,
            message="处理成功",
            data=result
        )
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        return BaseResponse(
            status=ResponseStatus.ERROR,
            message=str(e),
            data=None
        ) 