# 智能旅游推荐系统项目总结

## 1. 项目概述

这是一个基于大语言模型和向量数据库的智能旅游推荐系统。系统能够理解用户需求，提供个性化的旅游景点和路线推荐。

## 2. 系统架构

### 2.1 核心组件
- **FastAPI**: Web API 框架
- **SQLAlchemy**: 数据库 ORM
- **FAISS**: 向量数据库
- **SentenceTransformer**: 文本向量化
- **Qwen**: 大语言模型服务

### 2.2 主要模块
1. **API 层** (`app/api/`)
   - 处理 HTTP 请求
   - 路由管理
   - 请求验证

2. **服务层** (`app/services/`)
   - `qwen_service.py`: 大语言模型服务
   - `vector_store.py`: 向量数据库服务
   - `rag_service.py`: RAG (检索增强生成) 服务
   - `tools.py`: 工具函数集合

3. **数据层** (`app/db/`)
   - 数据库模型
   - 会话管理
   - 数据迁移

4. **核心层** (`app/core/`)
   - 配置管理
   - 日志系统
   - 工具注册器

## 3. 功能特性

### 3.1 智能对话
- 多轮对话支持
- 上下文理解
- 意图识别
- 工具调用

### 3.2 旅游推荐
- 景点搜索
- 路线规划
- 个性化推荐
- 深度搜索

### 3.3 知识增强
- RAG 技术应用
- 向量检索
- 上下文优化
- 查询增强

## 4. 数据模型

### 4.1 景点 (Spot)
```python
- id: 主键
- name: 景点名称
- description: 描述
- location: 位置
- images: 图片列表
- tags: 标签列表
- rating: 评分
- vector_embedding: 向量嵌入
```

### 4.2 路线 (Route)
```python
- id: 主键
- name: 路线名称
- description: 描述
- spots: 景点列表
```

### 4.3 聊天历史 (ChatHistory)
```python
- id: 主键
- session_id: 会话ID
- user_query: 用户查询
- assistant_response: 助手回复
```

### 4.4 向量索引 (VectorIndex)
```python
- id: 主键
- collection_name: 集合名称
- record_id: 记录ID
- vector: 向量数据
- meta_info: 元数据
```

## 5. 工具函数

### 5.1 基础工具
- `general_tool`: 通用工具
- `search_spot_info`: 景点信息搜索
- `spot_recommend`: 景点推荐
- `spot_route_recommend`: 路线推荐
- `deep_search`: 深度搜索
- `add_required_spot`: 添加必选景点
- `travel_tips`: 旅行贴士

### 5.2 向量搜索工具
- `search_similar_spots`: 搜索相似景点
- `search_similar_routes`: 搜索相似路线

## 6. 技术特点

### 6.1 RAG 技术应用
- 使用向量数据库存储景点和路线信息
- 基于相似度检索相关文档
- 将检索到的信息用于增强查询
- 优化 LLM 的响应质量

### 6.2 向量数据库
- 使用 FAISS 实现高效的向量检索
- 支持多集合管理（spots/routes）
- 保存向量数据和元数据
- 提供相似度搜索功能

### 6.3 对话优化
- 多轮对话内容总结
- 上下文优化
- 意图识别
- 工具选择

## 7. 部署和初始化

### 7.1 数据库初始化
```bash
./scripts/init_db.py
```

### 7.2 向量数据库初始化
```bash
./scripts/init_vector_store.py
```

### 7.3 环境要求
- Python 3.12+
- SQLite 数据库
- 相关 Python 包依赖

## 8. 使用流程

1. 用户发送查询
2. 系统优化对话内容
3. 识别用户意图
4. 选择合适工具
5. 执行工具调用
6. 返回处理结果

## 9. 未来优化方向

1. 添加更多旅游相关工具
2. 优化向量检索性能
3. 增强 RAG 效果
4. 添加用户反馈机制
5. 支持更多数据源
6. 优化对话体验 