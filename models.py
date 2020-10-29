from exts import db
from datetime import datetime
# 定义一些模型

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Issue(db.Model):
    __tablename__ = 'issue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('issues'))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())

    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    issue = db.relationship('Issue', backref=db.backref('comments', order_by=create_time.desc()))
    author = db.relationship('User', backref=db.backref('comments'))