from sqlalchemy.orm import relationship, backref

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __init__(self, *args, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')


        self.username = username
        # 密码加密
        self.password = generate_password_hash(password)

    def check_password(self, raw_password):
        """
        验证数据库密码
        :param raw_password: 未加密的密码
        :return: true OR false
        调用方法：user.check_password(raw_password)
        """
        result = check_password_hash(self.password,raw_password)
        return result

class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # 关系反转
    author = db.relationship('User',backref=db.backref('topics'),order_by=create_time.desc())

class Claim(db.Model):
    __tablename__ = 'claim'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # 关系反转
    topic = db.relationship('Topic',backref=db.backref('claims',order_by=create_time.desc()))
    author = db.relationship('User',backref=db.backref('claims'))

class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'))
    claim_id = db.Column(db.Integer, db.ForeignKey('claim.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # 关系反转
    claim = db.relationship('Claim',backref=db.backref('replies',order_by=create_time.desc()))
    author = db.relationship('User',backref=db.backref('replies'))

