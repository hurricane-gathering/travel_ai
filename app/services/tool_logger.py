from app.core.logger import logger
from typing import Dict, Any
import json

class ToolLogger:
    @staticmethod
    def log_tool_selection(json_result: Dict[str, Any], query: str):
        """记录模型选择的工具"""
        try:
            action_type = json_result.get("actionType")
            functions = json_result.get("functions", [])
            
            logger.info("模型工具选择记录:")
            logger.info(f"用户查询: {query}")
            logger.info(f"执行类型: {action_type}")
            
            for idx, func in enumerate(functions, 1):
                func_name = func.get("funcName")
                params = func.get("parameters", [])
                params_str = ", ".join([f"{p.get('name')}={p.get('value')}" for p in params])
                logger.info(f"工具 {idx}: {func_name}({params_str})")
                
        except Exception as e:
            logger.error(f"工具选择记录失败: {str(e)}")

tool_logger = ToolLogger() 