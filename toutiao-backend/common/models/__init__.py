# from flask_sqlalchemy import SQLAlchemy
from .db_routing.routing_sqlalchemy import RoutingSQLAlchemy

# 创建数据库连接对象
db = RoutingSQLAlchemy()