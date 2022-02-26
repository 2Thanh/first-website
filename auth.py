from flask import Blueprint, render_template,redirect, url_for,request,flash,session
from . import db
from . models import User
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash




auth= Blueprint("auth",__name__)#
@auth.route("/Login", methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password): # if password hash=password
                flash("Loggined in", category="success")              
                login_user(user,remember=1)# remember là để lưu trạng thái đăng nhập
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect",category="error")
        else:
            flash("User did not exist",category="error")
    return render_template("Login.html", user=current_user)# de cho user vao duoc html
@auth.route("/Signup", methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("Signup.html", user=current_user)
@auth.route("/logout")
@login_required # login_required là hàm để kiểm tra đăng nhập chưa
def logout():
    logout_user()# logout current user
    return redirect(url_for("views.home"))#views.home là địa chỉ cần dc truy cập đến trước khi đến home