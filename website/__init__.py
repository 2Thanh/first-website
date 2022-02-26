from re import S
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
#from flask_message import login_manager

db=SQLAlchemy()# để tạo ra 1 key để mã hóa session
DB_NAME= "database.db" # để tạo ra 1 key để mã hóa session



def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = "hello"# để tạo ra 1 key để mã hóa session
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")# /api là địa chỉ cần dc truy cập đến trước khi đến home
    app.register_blueprint(auth, url_prefix="/")
    create_database(app) #tạo database

    from .models import User,Post,Comment,Like,Dislike
    
    create_database(app)# create database

    login_manager= LoginManager()
    login_manager.login_view= "auth.login" # tránh chưa đăng nhập thì không được truy cập đến trang home
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
        if not path.exists("website/"+ DB_NAME):# nếu không tồn tại database thì tạo database
            db.create_all(app=app)