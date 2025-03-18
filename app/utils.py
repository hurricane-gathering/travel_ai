from config import client, MODEL_NAME, histories


async def get_content(prompt):
    messages = [{
        "role": "system",
        "content": "你是一个专业的出行推荐官"
    }]
    messages.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )
    return completion.choices[0].message.content


async def search_spot_info(spot_list):
    prompt = "搜索景点信息：{}并进行介绍".format(spot_list)
    return await get_content(prompt)


async def spot_recommend():
    prompt = "根据用户意图进行景点推荐"
    return await get_content(prompt)


async def spot_route_recommend(spot_name):
    prompt = "搜索景点{}信息进行路线推荐.".format(spot_name)
    return await get_content(prompt)


async def deep_search():
    prompt = "深度思考理解用户意图"
    return await get_content(prompt)


# async def add_option_spot(spot_name: str):
#     prompt = "Add {} to the option list.".format(spot_name)
#     messages = [{"role": "user", "content": prompt}]
#     return await get_content(messages)


# async def add_required_spot(spot_name: str):
#     prompt = "Add {} to the required list.".format(spot_name)
#     messages = [{"role": "user", "content": prompt}]
#     return await get_content(messages)


async def general_tool():
    prompt = "深度思考理解用户意图"
    return await get_content(prompt)


tool_funcs = [general_tool, search_spot_info,
              spot_recommend, spot_route_recommend, deep_search]


async def execute_tool(call_str):
    # 解析工具名和参数字典
    print("call_str:", call_str)
    tool_name = call_str.split("(")[0]
    params_str = call_str.split("(")[1].rstrip(")")
    print("params_str:", params_str)
    params = {}
    if (params_str):
        for param in params_str.split(", "):
            key, value = param.split("=")
            params[key] = value.strip("'")

    tool_func = {func.__name__: func for func in tool_funcs}
    if tool_name not in tool_func:
        raise ValueError("Unknown tool: " + tool_name)
    return await tool_func[tool_name](**params)
