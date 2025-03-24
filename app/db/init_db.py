from app.db.session import Base, engine
from app.db.models import Spot, Route, ChatHistory
import logging

logger = logging.getLogger(__name__)

def init_db() -> None:
    """初始化数据库"""
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise

if __name__ == "__main__":
    init_db() 