from openai import OpenAI
from app.tool import FUNCTION_CALLING_TOOLS, tool_desc, tool_names
from config import client, MODEL_NAME, histories


async def planning(prompt: str):
    messages = [{"role": "system", "content": "你是一个 Function Planner"}]
    messages.append({
        "role": "user",
        "content": prompt
    })
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )
    return completion.choices[0].message.content


async def function_planning(query: str):
    print(f"可调用工具数量：{len(FUNCTION_CALLING_TOOLS)}")

    prompt = f"""
解析用户意图: {query}。

你是一位资深旅行规划师，请根据用户输入及上下文，严格按以下规则输出工具名称及参数：

### 可用工具列表：
{tool_desc}

### 强制规则：
1. 工具名称必须从以下选择：[{tool_names}]，禁止编造新工具。
2. 参数需从输入中直接抽取，禁止自行生成或假设值。
3. 若需多工具协作，或无法匹配具体工具，输出 `general_tool()`。
4. 最终输出格式为：工具名(参数名='参数值')，例如 `spot_route_recommend(spot_name='上海')`。
5. 如果工具没有明确说明需要参数则不要带有参数输出，如果带有参数则严格按照给定参数进行输出。

### 示例：
用户输入: 上海一日游
输出: spot_route_recommend(spot_name='上海')

用户输入: 青岛栈桥的开放时间是？
输出: search_spot_info(spot_list=[青岛栈桥])

用户输入: 帮我推荐上海十个好玩的景点
输出: spot_recommend()

用户输入: 谢谢
输出: general_tool()
"""
    response = await planning(prompt)
    return response


async def optimization(message: list):
    # 多轮改写优化api
    messages = [{
        "role": "system",
        "content": "你是一个专业的大模型改写优化家,总结下面的多轮对话内容"
    }]
    messages.extend(message)
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )
    return completion.choices[0].message.content