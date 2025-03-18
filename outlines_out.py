from enum import Enum
from pydantic import BaseModel
import outlines
import os


QWEN_API_URL = "http://10.151.166.62:8000/v1"
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


class FuncName(str, Enum):
    spot = "search_spot_info"
    route = "spot_route_info"
    deep = "deep_search"
    add_required = "add_required_spot"
    common = "general_tool"


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
