import os
import sys
from sqlalchemy import inspect
import logging

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from app.db.session import Base, engine
from app.db.models import Spot, Route, ChatHistory, VectorIndex

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    """初始化数据库"""
    try:
        # 检查已注册的模型
        logger.info("已注册的模型:")
        for table in Base.metadata.tables.values():
            logger.info(f"- {table.name}")

        # 创建所有表
        Base.metadata.create_all(bind=engine)
        
        # 验证表是否创建成功
        inspector = inspect(engine)
        created_tables = inspector.get_table_names()
        logger.info("成功创建的表:")
        for table in created_tables:
            logger.info(f"- {table}")
            columns = inspector.get_columns(table)
            logger.info(f"  列: {[col['name'] for col in columns]}")
            
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise

if __name__ == "__main__":
    init_db()