from typing import Dict, List, Any, Union
from app.core.logger import logger
from app.core.tools import tool_registry
from app.services.tools import tool_funcs
from app.services.tool_logger import tool_logger
from app.db.session import Session
from app.db.models import ChatHistory
import json
from enum import Enum

class ActionType(str, Enum):
    single = "singleFunction"
    multi = "multiFunction"

class ToolExecutor:
    """工具执行器"""
    
    @staticmethod
    async def execute_single_function(function_info: Dict, optimized_content: str = "") -> Any:
        """执行单个工具函数"""
        try:
            func_name = function_info.get("funcName")
            if not func_name:
                logger.error("未指定工具函数名称")
                return None
                
            # 获取工具函数
            tool_func = tool_registry.get_tool(func_name)
            if not tool_func:
                logger.error(f"未找到工具函数: {func_name}")
                return await tool_registry.get_tool("general_tool")(query=str(function_info))
            
            # 处理参数
            parameters = {p["name"]: p["value"] for p in function_info.get("parameters", [])}
            
            # 添加优化内容到参数中
            if optimized_content:
                parameters["summary"] = optimized_content
                
            logger.info(f"执行工具函数: {func_name}, 参数: {parameters}")
            result = await tool_func(**parameters)
            
            # 保存执行记录
            with Session() as session:
                history = ChatHistory(
                    session_id="tool_execution",  # 使用固定的会话ID标识工具执行
                    user_query="",  # 工具执行不需要用户查询
                    assistant_response=f"工具 {func_name} 执行结果: {result}"  # 将结果存储在助手回复字段
                )
                session.add(history)
                session.commit()
                
            return result
            
        except Exception as e:
            logger.error(f"工具函数执行失败: {str(e)}")
            return None
            
    @staticmethod
    async def execute_multi_functions(functions: List[Dict], optimized_content: str = "") -> List[Any]:
        """执行多个工具函数"""
        results = []
        for func_info in functions:
            result = await ToolExecutor.execute_single_function(func_info, optimized_content)
            results.append(result)
        return results

# async def execute_single_function(func_name: str, params: Dict[str, Any], summary: str) -> str:
#     """执行单一功能"""
#     if func_name not in tool_funcs:
#         raise ValueError(f"未知工具: {func_name}")
    
#     params["summary"] = summary
#     return await tool_funcs[func_name](**params)

# async def execute_multi_function(functions: List[Dict[str, Any]], summary: str) -> str:
#     """执行多功能调用，串联结果"""
#     results = []
#     current_summary = summary
    
#     for func_call in functions:
#         func_name = func_call.get("funcName")
#         params = {param.get("name"): param.get("value") for param in func_call.get("parameters", [])}
#         params["summary"] = current_summary
        
#         if func_name not in tool_funcs:
#             raise ValueError(f"未知工具: {func_name}")
        
#         result = await tool_funcs[func_name](**params)
#         results.append(result)
#         current_summary = f"{current_summary}\n{result}"
    
#     return "\n".join(results)

async def execute_tool(response: str, optimized_content: str = "", query: str = "") -> str:
    """执行工具调用"""
    try:
        # 解析模型返回的JSON
        try:
            function_call = json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"JSON解析失败: {response}")
            return await tool_registry.get_tool("general_tool")(query=query)
        
        # 根据actionType执行不同的调用逻辑
        action_type = function_call.get("actionType", "")
        functions = function_call.get("functions", [])
        
        if not functions:
            logger.error("未找到要执行的工具函数")
            return await tool_registry.get_tool("general_tool")(query=query)
            
        if action_type == "singleFunction":
            result = await ToolExecutor.execute_single_function(functions[0], optimized_content)
            return str(result) if result else "工具执行失败"
            
        elif action_type == "multiFunction":
            results = await ToolExecutor.execute_multi_functions(functions, optimized_content)
            # 合并多个工具的执行结果
            combined_result = "\n".join([str(r) for r in results if r])
            return combined_result if combined_result else "工具执行失败"
            
        else:
            logger.error(f"未知的actionType: {action_type}")
            return await tool_registry.get_tool("general_tool")(query=query)
            
    except Exception as e:
        logger.error(f"工具执行失败: {str(e)}")
        return await tool_registry.get_tool("general_tool")(query=query) 