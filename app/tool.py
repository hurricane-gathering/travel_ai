FUNCTION_CALLING_TOOLS = [
    {
        "name_for_model": "search_spot_info",
        "name_for_human": "查询景点信息",
        "description_for_human": "根据关键词搜索景点详情（如开放时间、票价）",
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
        "description_for_human": "根据用户输入内容推荐景点",
        "parameters": []
    },
    {
        "name_for_model": "spot_route_recommend",
        "name_for_human": "景点路线推荐",
        "description_for_human": "搜索指定景点的旅游路线信息并整理推荐给用户",
        "parameters": [{
            "description": "需要查询的景点的名称",
            "name": "spot_name",
            "required": True,
            "schema": {
                "type": "string"
            }
        }]
    },
    {
        "name_for_model": "deep_search",
        "name_for_human": "深度思考",
        "description_for_human": "深度思考理解用户意图"
    },
    # {
    #     "name_for_model": "add_required_spot",
    #     "name_for_human": "添加必选景点",
    #     "description_for_human": "将指定景点加入用户的必选列表",
    #     "parameters": [{
    #         "description": "景点名称构成的列表，不同景点之间使用英文逗号连接;没有明确提到具体景点时，此参数取值为空字符串",
    #         "name": "spot_name",
    #         "required": True,
    #         "schema": {
    #             "type": "string",
    #         }
    #     }]
    # },
    # {
    #     "name_for_model": "add_option_spot",
    #     "name_for_human": "添加备选景点",
    #     "description_for_human": "将指定景点加入用户的备选列表",
    #     "parameters": [{
    #         "description": "备选景点名称构成的列表，不同景点之间使用英文逗号连接;没有明确提到具体景点时，此参数取值为空字符串",
    #         "name": "option_spot_list",
    #         "required": True,
    #         "schema": {
    #             "type": "string",
    #         }
    #     }]
    # },
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
                desc += f"\n- {param['name']}: {param['description']} (必填: {param['required']})"
                if "schema" in param:
                    desc += f"\n  - 返回类型: {param['schema']['type']})"
        tool_desc.append(desc)
        tool_names.append(tool["name_for_model"])

    return "\n".join(tool_desc), ", ".join(tool_names)


# 生成工具描述和名称列表
FUNCTION_CALLING_TOOL_DESC = "(name_for_model): Call this tool to interact with the (name_for_human) API. What is the (name_for_human) API useful for (description_for_human)?"
tool_desc, tool_names = parse_tool_text_info(
    FUNCTION_CALLING_TOOLS, FUNCTION_CALLING_TOOL_DESC)
