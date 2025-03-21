from apis.utils import function_planning, histories
from fastapi import APIRouter

from app.utils import execute_tool

router = APIRouter()


@router.post("/query")
async def process_query(user_query: str):
    """处理用户查询，执行相应 API 逻辑"""
    user_input = user_query
    histories.append({"role": "user", "content": user_input})
    # 1. 解析用户意图
    planning_result = await function_planning(user_input)
    histories.append({"role": "assistant", "content": planning_result})
    print(planning_result)
    # 2. 执行工具
    res = await execute_tool(planning_result)
    histories.append({"role": "assistant", "content": res})
    print(f"histories: {histories} \n")
    return planning_result, res
