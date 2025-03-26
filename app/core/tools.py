from typing import List, Dict, Any
from app.core.logger import logger
from app.models.base import SpotInfo, RouteInfo
from app.db.session import Session
from app.db.crud import create_spot, get_spots, create_route
import json
from app.services.tools import tool_funcs

# 工具描述
# tool_desc = """
# 可用工具函数列表:
# 1. search_spot_info: 搜索景点信息
#    - 参数: spot_list (景点列表)
   
# 2. spot_recommend: 景点推荐
#    - 参数: season (季节), days (天数), preference (偏好)
   
# 3. spot_route_recommend: 路线规划
#    - 参数: spot_name (景点名称), transport (交通方式), time_budget (时间预算)
   
# 4. deep_search: 深度搜索
#    - 参数: focus (关注点)
   
# 5. add_required_spot: 添加必选景点
#    - 参数: spot_name (景点名称), reason (原因)
   
# 6. travel_tips: 旅行贴士
#    - 参数: destination (目的地), aspect (关注方面)
   
# 7. general_tool: 通用工具
#    - 参数: query (查询内容)
# """

class ToolRegistry:
    """工具注册器"""
    
    def __init__(self):
        self._tools = {}
        
    def register(self, name: str, func: callable):
        """注册工具函数"""
        self._tools[name] = func
        logger.info(f"注册工具函数: {name}")
        
    def get_tool(self, name: str) -> callable:
        """获取工具函数"""
        return self._tools.get(name)
        
    def list_tools(self) -> List[str]:
        """列出所有工具"""
        return list(self._tools.keys())

# 创建工具注册器实例
tool_registry = ToolRegistry()

# 注册所有工具
for tool_name, tool_func in tool_funcs.items():
    tool_registry.register(tool_name, tool_func)

logger.info(f"可调用工具数量：{len(tool_registry.list_tools())}")

# async def search_spots(query: str) -> List[Dict]:
#     """搜索景点信息"""
#     logger.info(f"搜索景点: {query}")
#     try:
#         with Session() as session:
#             spots = get_spots(session, query)
#             return [spot.to_dict() for spot in spots]
#     except Exception as e:
#         logger.error(f"搜索景点失败: {str(e)}")
#         return []

# async def plan_route(spots: List[str]) -> Dict:
#     """规划景点路线"""
#     logger.info(f"规划路线: {spots}")
#     try:
#         # 这里可以添加实际的路线规划算法
#         route = RouteInfo(
#             spots=spots,
#             order=list(range(len(spots))),
#             duration="1天",
#             description=f"包含景点: {', '.join(spots)}"
#         )
#         return route.to_dict()
#     except Exception as e:
#         logger.error(f"路线规划失败: {str(e)}")
#         return {}

# async def add_spot(name: str, description: str, location: str) -> Dict:
#     """添加新景点"""
#     logger.info(f"添加景点: {name}")
#     try:
#         spot = SpotInfo(
#             name=name,
#             description=description,
#             location=location
#         )
#         with Session() as session:
#             new_spot = create_spot(session, spot)
#             return new_spot.to_dict()
#     except Exception as e:
#         logger.error(f"添加景点失败: {str(e)}")
#         return {}

FUNCTION_CALLING_TOOLS = [
    {
        "name_for_model": "search_spot_info",
        "name_for_human": "查询景点信息",
        "description_for_human": "根据关键词搜索景点详情（如开放时间、票价、交通方式等实用信息）",
        "parameters": [{
            "description": "景点名称列表,不同景点之间使用英文逗号连接",
            "name": "spot_list",
            "required": True,
            "schema": {
                "type": "list",
            }
        }]
    },
    {
        "name_for_model": "spot_recommend",
        "name_for_human": "景点推荐",
        "description_for_human": "根据用户需求推荐合适的景点",
        "parameters": [
            {
                "description": "旅行季节",
                "name": "season",
                "required": False,
                "schema": {"type": "string"}
            },
            {
                "description": "行程天数",
                "name": "days",
                "required": False,
                "schema": {"type": "string"}
            },
            {
                "description": "偏好类型（如历史、自然、文化等）",
                "name": "preference",
                "required": False,
                "schema": {"type": "string"}
            }
        ]
    },
    {
        "name_for_model": "spot_route_recommend",
        "name_for_human": "路线推荐",
        "description_for_human": "规划详细的景点游览路线",
        "parameters": [
            {
                "description": "需要规划路线的景点名称",
                "name": "spot_name",
                "required": True,
                "schema": {"type": "string"}
            },
            {
                "description": "交通方式",
                "name": "transport",
                "required": False,
                "schema": {"type": "string"}
            },
            {
                "description": "游览时间预算",
                "name": "time_budget",
                "required": False,
                "schema": {"type": "string"}
            }
        ]
    },
    {
        "name_for_model": "deep_search",
        "name_for_human": "深度思考",
        "description_for_human": "深度分析用户需求并提供个性化建议",
        "parameters": [{
            "description": "重点关注的方面（如文化体验、美食、活动等）",
            "name": "focus",
            "required": False,
            "schema": {"type": "string"}
        }]
    },
    {
        "name_for_model": "add_required_spot",
        "name_for_human": "添加必选景点",
        "description_for_human": "将指定景点添加到必选景点列表",
        "parameters": [
            {
                "description": "景点名称",
                "name": "spot_name",
                "required": True,
                "schema": {"type": "string"}
            },
            {
                "description": "添加原因",
                "name": "reason",
                "required": False,
                "schema": {"type": "string"}
            }
        ]
    },
    {
        "name_for_model": "travel_tips",
        "name_for_human": "旅行贴士",
        "description_for_human": "提供目的地的实用旅行建议",
        "parameters": [
            {
                "description": "目的地名称",
                "name": "destination",
                "required": True,
                "schema": {"type": "string"}
            },
            {
                "description": "需要建议的具体方面",
                "name": "aspect",
                "required": False,
                "schema": {"type": "string"}
            }
        ]
    },
    {
        "name_for_model": "general_tool",
        "name_for_human": "通用工具",
        "description_for_human": "处理无需具体操作的场景（如致谢、默认响应）"
    }
]

def parse_tool_text_info(tools, template):
    tool_desc = []
    tool_names = []
    for tool in tools:
        desc = template.replace("(name_for_model)", tool["name_for_model"]) \
                       .replace("(name_for_human)", tool["name_for_human"]) \
                       .replace("(description_for_human)", tool["description_for_human"])

        # 添加参数描述
        if "parameters" in tool and tool["parameters"]:
            desc += "\n参数："
            for param in tool["parameters"]:
                desc += f"\n- {param['name']}: {param['description']} (是否必填: {param['required']})"
                if "schema" in param:
                    desc += f"\n  - 参数类型: {param['schema']['type']})"
        tool_desc.append(desc)
        tool_names.append(tool["name_for_model"])

    return "\n".join(tool_desc), ", ".join(tool_names)

# 生成工具描述和名称列表
FUNCTION_CALLING_TOOL_DESC = "(name_for_model): Call this tool to interact with the (name_for_human) API. What is the (name_for_human) API useful for (description_for_human)?"
tool_desc, tool_names = parse_tool_text_info(FUNCTION_CALLING_TOOLS, FUNCTION_CALLING_TOOL_DESC) 