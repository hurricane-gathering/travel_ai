from apis.utils import optimization
from config import client, MODEL_NAME, histories


async def get_content(message: list):
    messages = [{
        "role": "system",
        "content": "你是一个专业的出行推荐官"
    }]
    messages.extend(message)
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )
    return completion.choices[0].message.content


async def search_spot_info(**kwargs):
    spot_list = kwargs["spot_list"]
    summary = kwargs["summary"]
    messages = [
        {"role": "assistant", "content": summary},
        {"role": "user", "content": f"根据关键词{spot_list}搜索景点详情"}]
    return await get_content(messages)


async def spot_recommend(**kwargs):
    summary = kwargs.get('summary') or ''
    messages = [
        {"role": "assistant", "content": summary},
        {"role": "user", "content": "根据上文提供的关键词进行景点推荐"}]
    return await get_content(messages)


async def spot_route_recommend(**kwargs):
    summary = kwargs.get('summary') or ''
    spot_name = kwargs["spot_name"]
    messages = [
        {"role": "assistant", "content": summary},
        {"role": "user", "content": f"搜索{spot_name}的出行路线"}]
    return await get_content(messages)


async def deep_search(**kwargs):
    summary = kwargs.get('summary') or ''
    messages = [{'role': 'assistant', 'content': summary},
                {"role": "user", "content": "根据上文深度思考理解并给出相关的出行指南"}]
    return await get_content(messages)


async def general_tool(**kwargs):
    summary = kwargs.get('summary') or ''
    messages = [{'role': 'assistant', 'content': summary},
                {"role": "user", "content": "根据上文回答问题并给出通用解答"}]
    return await get_content(messages)


tool_funcs = [general_tool, search_spot_info,
              spot_recommend, spot_route_recommend, deep_search]


async def execute_tool(call_str):
    summary = await optimization(histories)
    # 解析工具名和参数字典
    tool_name = call_str.split("(")[0]
    params_str = call_str.split("(")[1].rstrip(")")
    params = {"summary": summary}
    if (params_str):
        for param in params_str.split(", "):
            key, value = param.split("=")
            params[key] = value.strip("'")

    tool_func = {func.__name__: func for func in tool_funcs}
    if tool_name not in tool_func:
        raise ValueError("Unknown tool: " + tool_name)
    return await tool_func[tool_name](**params)
