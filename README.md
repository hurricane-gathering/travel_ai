## 技术架构

### 后端技术栈
- **Web 框架**: FastAPI
- **数据库**: SQLAlchemy ORM + SQLite
- **大模型集成**: 通义千问 API
- **API 文档**: Swagger/OpenAPI

### 核心模块
- `app/api/`: API 路由和端点定义
- `app/core/`: 核心配置和工具函数
  - 配置管理
  - 日志系统
  - 工具注册器
- `app/models/`: 数据模型
  - 景点信息模型
  - 路线规划模型
  - 对话历史模型
- `app/services/`: 服务层
  - 大模型服务
  - 工具执行器
  - 数据处理服务

### 数据模型
- **Spot**: 景点信息
  - 基础信息（名称、描述、位置）
  - 媒体资源（图片）
  - 标签系统
  - 评分机制
- **Route**: 路线信息
  - 景点列表
  - 访问顺序
  - 交通方式
  - 时间和成本估算
- **ChatHistory**: 对话历史
  - 角色标识
  - 对话内容
  - 时间戳

## 项目特点

1. **模块化设计**
   - 清晰的代码结构
   - 高内聚低耦合
   - 易于扩展和维护

2. **智能化处理**
   - 自然语言理解
   - 多轮对话优化
   - 个性化推荐

3. **数据持久化**
   - 完整的数据模型
   - 事务支持
   - 时间戳追踪

4. **工具系统**
   - 灵活的工具注册机制
   - 支持单功能和多功能调用
   - 完善的错误处理

## 快速开始

1. **环境准备**
   ```bash
   pip install -r requirements.txt
   ```

2. **初始化数据库**
   ```bash
   python app/db/init_db.py
   ```

3. **启动服务**
   ```bash
   uvicorn app.main:app --reload --port 3040
   ```

## API 文档

启动服务后访问：
- Swagger UI: `http://localhost:3040/docs`
- ReDoc: `http://localhost:3040/redoc`


# 基于 function plan 的旅游景点/路线/推荐
1. 获取用户输入，经过 function planning 决策调用 funcName，function planning 采用function calling 范式调用格式

2. 经过多轮改写 api 总结历史对话信息

3. 得到function name及参数后执行该工具

4. 整合结果，加入历史对话

模块化
多轮对话上下文管理和多轮 summary api （管理优化对话上下文信息）
function planning （意图识别，调用能力）
 RAG 模块 （检索最相关的信息重构上下文）
Tools api 模块 （调用专有能力处理）
数据库管理模块 （作为元数据存储及历史对话记录）
向量数据库管理模块 （存储元数据及其向量化数据）

技术点：
fastapi、LLM api、意图识别算法、RAG、向量数据库，sqlalchemy、function calling、MCP协议、多路并行API调用