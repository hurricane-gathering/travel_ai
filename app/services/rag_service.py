from app.core.logger import logger
from app.services.vector_store import vector_store
from app.services.qwen_service import qwen_service

class RAGService:
    async def enhance_query(self, query: str) -> str:
        """增强查询"""
        try:
            # 1. 从向量数据库检索相关文档
            spot_docs = vector_store.search("spots", query, k=2)
            route_docs = vector_store.search("routes", query, k=1)
            
            if not spot_docs and not route_docs:
                return query
                
            # 2. 构建上下文
            context_parts = []
            
            # 添加景点信息
            if spot_docs:
                spot_context = "相关景点信息：\n"
                for doc in spot_docs:
                    spot_context += f"- {doc['metadata']['name']}: {doc['metadata'].get('description', '')}\n"
                context_parts.append(spot_context)
            
            # 添加路线信息
            if route_docs:
                route_context = "相关路线信息：\n"
                for doc in route_docs:
                    route_context += f"- {doc['metadata']['name']}: {doc['metadata'].get('description', '')}\n"
                context_parts.append(route_context)
            
            context = "\n".join(context_parts)
            
            # 3. 使用 LLM 增强查询
            prompt = f"""基于以下上下文信息，增强用户查询以获取更准确的搜索结果。

上下文信息：
{context}

用户查询：{query}

请生成一个更详细和准确的查询。保持查询简洁，只返回增强后的查询文本。"""

            messages = [
                {"role": "system", "content": "你是一个专业的查询优化助手，负责增强用户查询以获得更准确的搜索结果。"},
                {"role": "user", "content": prompt}
            ]
            
            enhanced_query = await qwen_service.create_completion(messages)
            logger.info(f"查询增强: {query} -> {enhanced_query}")
            
            return enhanced_query.strip()
            
        except Exception as e:
            logger.error(f"查询增强失败: {str(e)}")
            return query

rag_service = RAGService() 