from openai import OpenAI
from app.tool import FUNCTION_CALLING_TOOLS, tool_desc, tool_names
from config import client, MODEL_NAME, histories


async def planning(prompt: str):
    histories.append({
        "role": "user",
        "content": prompt
    })
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=histories
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
4. 最终输出格式为：工具名(参数名='参数值')，例如 `add_required_spot(spot_name='野生动物园')`。

### 示例：
用户输入: 将野生动物园加入必选
输出: add_required_spot(spot_name='野生动物园')

用户输入: 青岛栈桥的开放时间是？
输出: search_spot_info(spot_list=[青岛栈桥])

用户输入: 帮我推荐上海十个好玩的景点
输出: spot_recommend()

用户输入: 谢谢
输出: general_tool()
"""
    response = await planning(prompt)
    return response
