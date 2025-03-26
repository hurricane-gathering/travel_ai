from typing import List, Dict, Any, Optional
from app.core.logger import logger
from app.db.session import Session
from app.db.models import VectorIndex, Spot, Route, ChatHistory
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json

class VectorStore:
    """向量存储服务"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # 向量维度
        self.indices = {}  # 集合名称 -> FAISS索引的映射
        
    def init_index(self, collection_name: str):
        """初始化FAISS索引"""
        if collection_name not in self.indices:
            index = faiss.IndexFlatL2(self.dimension)
            self.indices[collection_name] = index
            logger.info(f"创建向量索引: {collection_name}")
            
    def get_embedding(self, text: str) -> np.ndarray:
        """获取文本的向量嵌入"""
        return self.model.encode(text)
        
    def add_to_index(self, collection_name: str, record_id: int, text: str, metadata: Dict = None):
        """添加记录到向量索引"""
        try:
            # 获取向量嵌入
            vector = self.get_embedding(text)
            
            # 确保索引存在
            self.init_index(collection_name)
            
            # 添加到FAISS索引
            self.indices[collection_name].add(np.array([vector]))
            
            # 保存到数据库
            with Session() as session:
                vector_index = VectorIndex(
                    collection_name=collection_name,
                    record_id=record_id,
                    vector=vector.tolist(),  # 转换为列表以便JSON序列化
                    meta_info=metadata or {}
                )
                session.add(vector_index)
                session.commit()
                
            logger.info(f"添加向量索引记录: {collection_name}/{record_id}")
            
        except Exception as e:
            logger.error(f"添加向量索引失败: {str(e)}")
            raise
            
    def search(self, collection_name: str, query: str, k: int = 5) -> List[Dict]:
        """搜索最相似的记录"""
        try:
            # 获取查询向量
            query_vector = self.get_embedding(query)
            
            # 检查数据库中的记录数量
            with Session() as session:
                record_count = session.query(VectorIndex).filter(
                    VectorIndex.collection_name == collection_name
                ).count()
                
                if record_count == 0:
                    logger.warning(f"集合 {collection_name} 中没有记录")
                    return []
                    
                # 如果索引不存在，从数据库重建索引
                if collection_name not in self.indices:
                    logger.info(f"从数据库重建集合 {collection_name} 的索引")
                    self.rebuild_index(collection_name)
            
            # 执行搜索
            D, I = self.indices[collection_name].search(
                np.array([query_vector]), 
                min(k, record_count)  # 确保k不超过记录数量
            )
            
            # 获取结果
            results = []
            with Session() as session:
                # 获取该集合的所有向量索引记录
                vector_indices = session.query(VectorIndex).filter(
                    VectorIndex.collection_name == collection_name
                ).all()
                
                # 使用FAISS返回的索引位置获取对应的记录
                for i, (distance, idx) in enumerate(zip(D[0], I[0])):
                    if idx < 0 or idx >= len(vector_indices):  # FAISS返回-1表示无效结果
                        continue
                        
                    vector_index = vector_indices[idx]
                    results.append({
                        "record_id": vector_index.record_id,
                        "distance": float(distance),
                        "metadata": vector_index.meta_info
                    })
                    
            logger.info(f"向量搜索结果 [{collection_name}]: {results}")
            return results
            
        except Exception as e:
            logger.error(f"向量搜索失败: {str(e)}")
            raise
            
    def rebuild_index(self, collection_name: str):
        """重建向量索引"""
        try:
            # 清除现有索引
            if collection_name in self.indices:
                del self.indices[collection_name]
            
            # 初始化新索引
            self.init_index(collection_name)
            
            # 从数据库加载所有记录
            with Session() as session:
                vectors = session.query(VectorIndex).filter(
                    VectorIndex.collection_name == collection_name
                ).all()
                
                if vectors:
                    # 重建FAISS索引
                    all_vectors = np.array([np.array(v.vector) for v in vectors])
                    self.indices[collection_name].add(all_vectors)
                    logger.info(f"重建向量索引完成: {collection_name}, 添加了 {len(vectors)} 条记录")
                else:
                    logger.warning(f"集合 {collection_name} 中没有记录，无法重建索引")
            
        except Exception as e:
            logger.error(f"重建向量索引失败: {str(e)}")
            raise

# 创建向量存储实例
vector_store = VectorStore() 