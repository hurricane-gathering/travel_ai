import asyncio
from app.db.session import Session
from app.db.models import Spot, Route
from app.core.logger import logger

async def init_db():
    """初始化数据库，添加示例数据"""
    try:
        with Session() as session:
            # 1. 添加景点
            spots = [
                Spot(
                    name="故宫",
                    description="故宫是中国明清两代的皇家宫殿，是中国现存规模最大、保存最完整的木质结构古建筑群。",
                    location="北京市东城区景山前街4号",
                    tags=["历史", "文化", "建筑"],
                    rating=4.8
                ),
                Spot(
                    name="长城",
                    description="长城是中国古代伟大的防御工程，是中华民族的精神象征。八达岭长城是最著名的景区之一。",
                    location="北京市延庆区军都山关沟",
                    tags=["历史", "文化", "自然"],
                    rating=4.9
                ),
                Spot(
                    name="天坛",
                    description="天坛是中国古代皇帝祭天的场所，是中国现存规模最大、保存最完整的古代祭天建筑群。",
                    location="北京市东城区天坛路甲1号",
                    tags=["历史", "文化", "建筑"],
                    rating=4.7
                ),
                Spot(
                    name="颐和园",
                    description="颐和园是中国现存规模最大、保存最完整的皇家园林，被誉为'皇家园林博物馆'。",
                    location="北京市海淀区新建宫门路19号",
                    tags=["历史", "文化", "园林"],
                    rating=4.8
                )
            ]
            
            for spot in spots:
                session.add(spot)
            session.commit()
            logger.info(f"添加了 {len(spots)} 个景点")
            
            # 2. 添加路线
            routes = [
                Route(
                    name="北京经典一日游",
                    description="游览故宫、天坛、颐和园等经典景点，体验北京历史文化。",
                    spots=["故宫", "天坛", "颐和园"]
                ),
                Route(
                    name="长城文化之旅",
                    description="游览八达岭长城，体验古代军事防御工程。",
                    spots=["长城"]
                ),
                Route(
                    name="北京文化探索之旅",
                    description="深度游览故宫、天坛等文化景点，了解中国传统文化。",
                    spots=["故宫", "天坛"]
                )
            ]
            
            for route in routes:
                session.add(route)
            session.commit()
            logger.info(f"添加了 {len(routes)} 个路线")
            
        logger.info("数据库初始化完成")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db()) 