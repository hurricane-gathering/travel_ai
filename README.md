# 智能旅游推荐系统

基于 FastAPI 和通义千问（Qwen）大模型的智能旅游推荐系统，提供景点推荐、路线规划和智能对话等功能。

## 核心功能

### 1. 智能对话
- 基于通义千问大模型的自然语言交互
- 多轮对话历史记录和优化
- 上下文理解和意图识别

### 2. 景点推荐
- 智能景点搜索和筛选
- 基于用户偏好的个性化推荐
- 景点详细信息展示（位置、描述、标签等）
- 景点评分和评价系统

### 3. 路线规划
- 多景点智能路线规划
- 交通方式推荐
- 时间和成本估算
- 路线优化和调整

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
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **配置设置**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，配置必要的环境变量
   ```

3. **初始化数据库**
   ```bash
   python app/db/init_db.py
   ```

4. **启动服务**
   ```bash
   uvicorn app.main:app --reload --port 3040
   ```

## API 文档

启动服务后访问：
- Swagger UI: `http://localhost:3040/docs`
- ReDoc: `http://localhost:3040/redoc`

## 开发规范

- 遵循 PEP 8 Python 代码规范
- 使用 Git Flow 工作流
- 完整的单元测试覆盖
- 详细的代码注释和文档

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 发起 Pull Request

## 许可证

MIT License 