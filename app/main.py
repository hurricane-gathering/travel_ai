from openai import OpenAI
from enum import Enum
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import outlines
import os

app = FastAPI()

QWEN_API_URL = "http://10.151.166.62:8000/v1"
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
client = OpenAI(base_url=QWEN_API_URL, api_key="none")

messages = [
    {
        "role": "system",
        "content": "你是一个专业的出行推荐官"
    }
]


class UserQuery(BaseModel):
    query: str


class FuncName(str, Enum):
    spot = "spot"
    route = "route"
    deep = "deep"


class ActionType(str, Enum):
    single = "singleFunction"
    multi = "multiFunction"


class OutJson(BaseModel):
    funcName: FuncName
    actionType: ActionType


os.environ["OPENAI_API_BASE"] = QWEN_API_URL
model = outlines.models.transformers(MODEL_NAME)
generator = outlines.generate.json(model, OutJson)


async def call_qwen_api(prompt: str):
    res = generator(prompt)
    return res


async def get_content():
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )
    return completion.choices[0].message.content


async def function_planning(query: str):
    """分析用户的 query，返回任务类型"""
    prompt = f"解析用户意图: {query}。请返回一个 JSON 格式，包含 funcName 和 actionType"
    ""
    response = await call_qwen_api(prompt)
    return response.model_dump_json()


@app.post("/process_query")
async def process_query(user_query: UserQuery):
    """处理用户查询，执行相应 API 逻辑"""
    user_input = user_query.query

    # 1. 解析用户意图
    planning_result = await function_planning(user_input)
    planning_result = json.loads(planning_result)
    func_name = planning_result.get("funcName", "unknown")
    action_type = planning_result.get("actionType", "singleFunction")

    # 2. 处理不同任务
    if action_type == "singleFunction":
        return await handle_single_function(func_name, user_input)
    elif action_type == "multiFunction":
        return await handle_multi_function(func_name, user_input)
    else:
        raise HTTPException(status_code=400, detail="未知的 actionType")


async def handle_single_function(func_name: str, user_input: str):
    """处理单个 API 任务"""
    if func_name == "spot":
        return await spot_rec(user_input)
    elif func_name == "route":
        return await route_rec(user_input)
    elif func_name == "deep":
        return await deep_sear(user_input)
    else:
        return await other(user_input)


async def handle_multi_function(func_name: str, user_input: str):
    """处理多个 API 任务"""


async def spot_rec(user_input: str):
    """景点推荐"""
    prompt = f"根据用户输入: {user_input}。进行景点推荐"
    messages.append({"role": "user", "content": prompt})
    res = await get_content()
    return res


async def route_rec(user_input: str):
    """路径规划"""
    prompt = f"根据用户输入: {user_input}。进行回复，包含路径规划的起点和目的地以及途径地"
    messages.append({"role": "user", "content": prompt})
    res = await get_content()
    return res


async def deep_sear(user_input: str):
    """深度搜索"""
    prompt = f"根据用户输入: {user_input}。进行回复，包含搜索结果"
    messages.append({"role": "user", "content": prompt})
    res = await get_content()
    return res


async def other(user_input: str):
    """其他任务"""
    prompt = f"根据用户输入: {user_input}。进行回复"
    messages.append({"role": "user", "content": prompt})
    res = await get_content()
    return res



