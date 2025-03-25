from app.db.session import Session
from app.db.models import Spot, Route
from app.core.logger import logger

def init_test_data():
    """初始化测试数据"""
    try:
        with Session() as session:
            # 添加景点数据
            spots = [
                Spot(
                    name="兵马俑",
                    description='秦始皇陵兵马俑是世界八大奇迹之一，被誉为"世界第八大奇迹"，是中国最大的古墓葬群。',
                    location="西安市临潼区秦始皇陵东侧1.5公里处",
                    images=["bingmayong1.jpg", "bingmayong2.jpg"],
                    tags=["文化遗产", "历史遗迹", "必游景点"],
                    rating=4.8
                ),
                Spot(
                    name="大雁塔",
                    description='大雁塔是一座佛教建筑，始建于唐永徽四年（653年），是玄奘法师主持修建的，用来存放从印度取回的佛经。',
                    location="西安市雁塔区雁塔路",
                    images=["dayanta1.jpg", "dayanta2.jpg"],
                    tags=["佛教文化", "历史建筑", "地标"],
                    rating=4.6
                ),
                Spot(
                    name="回民街",
                    description='回民街是西安著名的美食街，汇集了各种陕西特色小吃，如羊肉泡馍、肉夹馍、各种烤肉等。',
                    location="西安市碑林区北院门内",
                    images=["huiminjie1.jpg", "huiminjie2.jpg"],
                    tags=["美食", "小吃", "购物"],
                    rating=4.7
                ),
                Spot(
                    name="古城墙",
                    description='西安古城墙是中国现存规模最大、保存最完整的古代城垣，也是世界上保存最完整的古代城垣。',
                    location="西安市碑林区环城南路",
                    images=["chengqiang1.jpg", "chengqiang2.jpg"],
                    tags=["历史遗迹", "城市地标", "必游景点"],
                    rating=4.9
                )
            ]
            session.add_all(spots)
            session.commit()
            logger.info(f"添加了 {len(spots)} 个景点")
            
            # 添加路线数据
            routes = [
                Route(
                    name="西安经典一日游",
                    description="游览西安最具代表性的景点，体验历史文化与美食。",
                    spots=[{
                        "spot_id": 1,
                        "order": 1,
                        "duration": "3小时",
                        "notes": "建议上午先去兵马俑，人少一些"
                    }, {
                        "spot_id": 2,
                        "order": 2,
                        "duration": "2小时",
                        "notes": "可以在大雁塔北广场休息"
                    }, {
                        "spot_id": 3,
                        "order": 3,
                        "duration": "2小时",
                        "notes": "晚上去回民街品尝美食"
                    }]
                ),
                Route(
                    name="西安文化探索之旅",
                    description="深入了解西安的历史文化，感受古都魅力。",
                    spots=[{
                        "spot_id": 4,
                        "order": 1,
                        "duration": "2小时",
                        "notes": "建议早上或傍晚登城墙"
                    }, {
                        "spot_id": 2,
                        "order": 2,
                        "duration": "2小时",
                        "notes": "参观大雁塔佛教文化"
                    }, {
                        "spot_id": 1,
                        "order": 3,
                        "duration": "3小时",
                        "notes": "了解秦朝历史文化"
                    }]
                )
            ]
            session.add_all(routes)
            session.commit()
            logger.info(f"添加了 {len(routes)} 条路线")
            
    except Exception as e:
        logger.error(f"初始化测试数据失败: {str(e)}")
        raise

if __name__ == "__main__":
    init_test_data() 