from app.core.logger import logger
from app.services.vector_store import vector_store
from app.services.qwen_service import qwen_service
from typing import Dict, Any, List

class RAGService:
    # 搜索配置常量
    EXACT_MATCH_K = 1  # 精确匹配返回数量
    FUZZY_MATCH_K = 2  # 模糊匹配返回数量
    MULTI_MATCH_K = 3  # 多关键词匹配返回数量
    
    def __init__(self):
        # 定义工具名称到增强方法的映射
        self._enhance_methods = {
            "search_spot_info": self._enhance_spot_info_query,
            "spot_recommend": self._enhance_spot_recommend_query,
            "spot_route_recommend": self._enhance_route_recommend_query,
            "deep_search": self._enhance_deep_search_query,
            "general_tool": self._enhance_general_query
        }
    
    async def _search_spots(self, query: str, k: int = FUZZY_MATCH_K):
        """统一的景点搜索方法"""
        return vector_store.search("spots", query, k=k)
        
    async def _search_routes(self, query: str, k: int = FUZZY_MATCH_K):
        """统一的路线搜索方法"""
        return vector_store.search("routes", query, k=k)
    
    async def enhance_query(self, query: str, tool_name: str = None, **kwargs) -> str:
        """增强查询
        
        Args:
            query: 原始查询
            tool_name: 工具名称
            **kwargs: 工具特定参数
        """
        try:
            # 获取对应的增强方法
            enhance_method = self._enhance_methods.get(tool_name, self._enhance_general_query)
            
            # 获取历史对话
            histories = kwargs.get("histories", [])
            
            # 如果有历史对话，使用它们来优化当前查询
            if histories:
                query = await self._optimize_with_history(query, histories)
                
            # 使用工具特定方法进一步增强查询
            enhanced_query = await enhance_method(query, **kwargs)
            
            return enhanced_query
                
        except Exception as e:
            logger.error(f"查询增强失败: {str(e)}")
            return query
            
    async def _optimize_with_history(self, query: str, histories: List[Dict[str, str]]) -> str:
        """使用历史对话优化当前查询"""
        try:
            # 构建历史对话上下文
            context = "历史对话：\n"
            for h in histories:
                context += f"用户：{h.get('user', '')}\n"
                context += f"助手：{h.get('assistant', '')}\n"
                
            # 使用 LLM 优化查询
            prompt = f"""基于以下历史对话，优化当前用户的查询，使其更加明确和完整。

{context}

当前查询：{query}

请生成一个优化后的查询。保持查询简洁，只返回优化后的查询文本。"""

            messages = [
                {"role": "system", "content": "你是一个专业的旅游咨询助手，负责优化用户查询。"},
                {"role": "user", "content": prompt}
            ]
            
            optimized_query = await qwen_service.create_completion(messages)
            return optimized_query.strip()
            
        except Exception as e:
            logger.error(f"使用历史对话优化查询失败: {str(e)}")
            return query
            
    async def _enhance_spot_info_query(self, query: str, **kwargs) -> str:
        """增强景点信息查询"""
        spot_list = kwargs.get("spot_list", [])
        if not spot_list:
            return query
            
        # 检索相关景点信息
        spot_docs = []
        for spot in spot_list:
            # 使用景点名称进行精确匹配
            results = await self._search_spots(spot, k=self.EXACT_MATCH_K)
            if results:
                spot_docs.extend(results)
                
        if not spot_docs:
            # 如果没有找到精确匹配，尝试模糊搜索
            for spot in spot_list:
                results = await self._search_spots(spot, k=self.FUZZY_MATCH_K)
                if results:
                    spot_docs.extend(results)
                    
        if not spot_docs:
            return query
            
        # 构建上下文
        context = "相关景点信息：\n"
        for doc in spot_docs:
            context += f"- {doc['metadata']['name']}: {doc['metadata'].get('description', '')}\n"
            
        # 使用 LLM 增强查询
        prompt = f"""基于以下景点信息和用户查询，生成一个更详细的查询。

{context}

用户查询：{query}

请生成一个更详细的查询，重点关注门票价格、开放时间、交通方式等实用信息。保持查询简洁，只返回增强后的查询文本。"""

        messages = [
            {"role": "system", "content": "你是一个专业的旅游信息查询助手，负责获取景点的详细信息。"},
            {"role": "user", "content": prompt}
        ]
        
        enhanced_query = await qwen_service.create_completion(messages)
        return enhanced_query.strip()
        
    async def _enhance_spot_recommend_query(self, query: str, **kwargs) -> str:
        """增强景点推荐查询"""
        season = kwargs.get("season", "")
        days = kwargs.get("days", "")
        preference = kwargs.get("preference", "")
        
        # 构建检索条件
        search_terms = []
        if season:
            search_terms.append(season)
        if preference:
            search_terms.append(preference)
            
        # 检索相关景点
        spot_docs = []
        for term in search_terms:
            # 使用多个关键词进行检索
            results = await self._search_spots(term, k=self.MULTI_MATCH_K)
            if results:
                spot_docs.extend(results)
                
        if not spot_docs and query:
            # 如果没有找到相关景点，使用原始查询进行检索
            results = await self._search_spots(query, k=self.MULTI_MATCH_K)
            if results:
                spot_docs.extend(results)
                
        if not spot_docs:
            return query
            
        # 构建上下文
        context = "相关景点信息：\n"
        for doc in spot_docs:
            context += f"- {doc['metadata']['name']}: {doc['metadata'].get('description', '')}\n"
            
        # 使用 LLM 增强查询
        prompt = f"""基于以下信息和用户查询，生成一个更详细的查询。

{context}

用户查询：{query}
季节：{season}
天数：{days}
偏好：{preference}

请生成一个更详细的查询，重点关注符合用户偏好的景点推荐。保持查询简洁，只返回增强后的查询文本。"""

        messages = [
            {"role": "system", "content": "你是一个专业的景点推荐助手，负责推荐符合用户需求的景点。"},
            {"role": "user", "content": prompt}
        ]
        
        enhanced_query = await qwen_service.create_completion(messages)
        return enhanced_query.strip()
        
    async def _enhance_route_recommend_query(self, query: str, **kwargs) -> str:
        """增强路线推荐查询"""
        spot_name = kwargs.get("spot_name", "")
        transport = kwargs.get("transport", "")
        time_budget = kwargs.get("time_budget", "")
        
        # 检索相关路线
        route_docs = []
        if spot_name:
            # 使用景点名称进行精确匹配
            results = await self._search_routes(spot_name, k=self.FUZZY_MATCH_K)
            if results:
                route_docs.extend(results)
                
        if not route_docs and query:
            # 如果没有找到精确匹配，使用原始查询进行检索
            results = await self._search_routes(query, k=self.FUZZY_MATCH_K)
            if results:
                route_docs.extend(results)
                
        if not route_docs:
            return query
            
        # 构建上下文
        context = "相关路线信息：\n"
        for doc in route_docs:
            context += f"- {doc['metadata']['name']}: {doc['metadata'].get('description', '')}\n"
            
        # 使用 LLM 增强查询
        prompt = f"""基于以下信息和用户查询，生成一个更详细的查询。

{context}

用户查询：{query}
景点：{spot_name}
交通方式：{transport}
时间预算：{time_budget}

请生成一个更详细的查询，重点关注路线安排、时间分配、交通规划等。保持查询简洁，只返回增强后的查询文本。"""

        messages = [
            {"role": "system", "content": "你是一个专业的路线规划助手，负责设计合理的旅游路线。"},
            {"role": "user", "content": prompt}
        ]
        
        enhanced_query = await qwen_service.create_completion(messages)
        return enhanced_query.strip()
        
    async def _enhance_deep_search_query(self, query: str, **kwargs) -> str:
        """增强深度搜索查询"""
        focus = kwargs.get("focus", "")
        
        # 构建检索条件
        search_terms = [query]
        if focus:
            search_terms.append(focus)
            
        # 检索相关景点和路线
        spot_docs = []
        route_docs = []
        
        for term in search_terms:
            # 检索景点
            results = await self._search_spots(term, k=self.FUZZY_MATCH_K)
            if results:
                spot_docs.extend(results)
                
            # 检索路线
            results = await self._search_routes(term, k=self.EXACT_MATCH_K)
            if results:
                route_docs.extend(results)
                
        # 构建上下文
        context_parts = []
        
        if spot_docs:
            spot_context = "相关景点信息：\n"
            for doc in spot_docs:
                spot_context += f"- {doc['metadata']['name']}: {doc['metadata'].get('description', '')}\n"
            context_parts.append(spot_context)
            
        if route_docs:
            route_context = "相关路线信息：\n"
            for doc in route_docs:
                route_context += f"- {doc['metadata']['name']}: {doc['metadata'].get('description', '')}\n"
            context_parts.append(route_context)
            
        if not context_parts:
            return query
            
        context = "\n".join(context_parts)
        
        # 使用 LLM 增强查询
        prompt = f"""基于以下信息和用户查询，生成一个更详细的查询。

{context}

用户查询：{query}
关注点：{focus}

请生成一个更详细的查询，重点关注文化体验、地道美食、特色活动等深度游内容。保持查询简洁，只返回增强后的查询文本。"""

        messages = [
            {"role": "system", "content": "你是一个专业的深度游规划助手，负责提供深入的旅游体验建议。"},
            {"role": "user", "content": prompt}
        ]
        
        enhanced_query = await qwen_service.create_completion(messages)
        return enhanced_query.strip()
        
    async def _enhance_general_query(self, query: str) -> str:
        """增强通用查询"""
        # 构建检索条件
        search_terms = [query]
        
        # 检索相关景点和路线
        spot_docs = []
        route_docs = []
        
        for term in search_terms:
            # 检索景点
            results = await self._search_spots(term, k=self.FUZZY_MATCH_K)
            if results:
                spot_docs.extend(results)
                
            # 检索路线
            results = await self._search_routes(term, k=self.EXACT_MATCH_K)
            if results:
                route_docs.extend(results)
                
        # 构建上下文
        context_parts = []
        
        if spot_docs:
            spot_context = "相关景点信息：\n"
            for doc in spot_docs:
                spot_context += f"- {doc['metadata']['name']}: {doc['metadata'].get('description', '')}\n"
            context_parts.append(spot_context)
            
        if route_docs:
            route_context = "相关路线信息：\n"
            for doc in route_docs:
                route_context += f"- {doc['metadata']['name']}: {doc['metadata'].get('description', '')}\n"
            context_parts.append(route_context)
            
        if not context_parts:
            return query
            
        context = "\n".join(context_parts)
        
        # 使用 LLM 增强查询
        prompt = f"""基于以下信息和用户查询，生成一个更详细的查询。

{context}

用户查询：{query}

请生成一个更详细的查询。保持查询简洁，只返回增强后的查询文本。"""

        messages = [
            {"role": "system", "content": "你是一个专业的旅游咨询助手，负责提供准确的旅游信息和建议。"},
            {"role": "user", "content": prompt}
        ]
        
        enhanced_query = await qwen_service.create_completion(messages)
        return enhanced_query.strip()

rag_service = RAGService() 