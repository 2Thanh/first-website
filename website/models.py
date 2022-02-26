
from datetime import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)# primary_key tự động tăng id
    email=db.Column(db.String(100),unique=True) #unique là để email không trùng nhau
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    #DateTime(timezone=True) là để lấy thời gian hiện tại
    posts= db.relationship('Post',backref='user',passive_deletes=True)
    comments=db.relationship('Comment',backref='user',passive_deletes=True)
    likes=db.relationship('Like',backref='user',passive_deletes=True)
    dislike=db.relationship('Dislike',backref='user',passive_deletes=True)
    #backref là để lấy được user trong post
    #passive_delete là để khi xóa user thì xóa cả post của user đó
    #POST là để lấy được user khi post


class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    text= db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    author= db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)#foreign key là để liên kết giữa bảng user và bảng post
    comments=db.relationship('Comment',backref='post',passive_deletes=True)
    likes= db.relationship('Like',backref='post',passive_deletes=True)
    dislike=db.relationship('Dislike',backref='post',passive_deletes=True)
    # nullable là để nếu user không có bài viết thì không báo lỗi
    #ondelete là để xóa bài viết của bang User thì xóa cả bang Post của User đó
class Comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.String(200),nullable=False)#nullable là để nếu user không nhập comment thì không báo lỗi
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    author=db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey("post.id",ondelete="CASCADE"), nullable=False)
class Like(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    author=db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey("post.id",ondelete="CASCADE"), nullable=False)
class Dislike(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    author=db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey("post.id",ondelete="CASCADE"), nullable=False)
    