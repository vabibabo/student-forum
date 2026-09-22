
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
# 初始化SQLAlchemy对象
db = SQLAlchemy()
