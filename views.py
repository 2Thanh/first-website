from flask import Blueprint, render_template,request,flash,redirect,url_for,request
from flask_login import login_required, current_user
from . import db
from .models import User,Post,Comment,Like,Dislike
from werkzeug.utils import secure_filename
from __init__ import app
import os

views = Blueprint("views", __name__)
@views.route("/")
@views.route("/home")
@login_required
def home():
    print(current_user)
    posts=Post.query.all()
    comments=Comment.query.all()
    return render_template("home.html", user=current_user, posts=posts, comment=comments)
    
@views.route("/create_post", methods=["GET","POST"])
@login_required
def create_post():
    if request.method == "POST":
        text= request.form.get('text')
        if not text:
            flash("Post cannot be empty", category="error")
        else:
            post=Post(text=text,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("post created", category="success")
            #category=success de bao loi thanh cong
            return redirect(url_for("views.home"))# de chuyen ve trang home
    return render_template("create_post.html", user=current_user)
@views.route("/delete_posts/<id>")
@login_required
def delete_post(id):
    post=Post.query.filter_by(id=id).first()#lay ra gia tri dau tien cua id
    if not post:
        flash("Post not found", category="error")
    elif current_user.id != post.author :
        flash("you don't have permission to delete this post", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("post deleted", category="success")
    return redirect(url_for("views.home"))
@views.route("/posts/<username>")
@login_required
def posts(username):
    user=User.query.filter_by(username=username).first()
    posts=Post.query.filter_by(author=user.id).all()
    if username!=current_user.username:
        flash("you don't have permission to view this page", category="error")
        return redirect(url_for("views.home"))
    return render_template("posts.html", user=current_user, posts=posts, username=username)
@views.route("/create-comment/<post_id>",methods=["POST"])
@login_required
def comment_create(post_id):
        print("cai nay la",post_id)
        print("Tac gia la",current_user.id)
        text=request.form.get("text")
        if not text:
            flash("Comment cannot be empty", category="error")
        else:
            post=Post.query.filter_by(id=post_id)
            if post:
                comment=Comment(text=text, author=current_user.id, post_id=post_id)
                db.session.add(comment)
                db.session.commit()
            else:
                flash("post not found",category="error")
        return redirect(url_for("views.home"))
@views.route("/delete_comments/<id>")
@login_required
def delete_comment(id):
    comment=Comment.query.filter_by(id=id).first()
    if not comment:
        flash("comment not found",category="error")
    elif comment.author != current_user.id:
        flash("you don't have permission to delete this comment", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("comment deleted", category="success")
    return redirect(url_for("views.home"))


@views.route('/post_image')
@login_required
def upload_form():
	return render_template('post_image.html')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@views.route('/post_image', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part', category='error')
		return redirect(request.url)
	file = request.files['file']

	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.file)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below',category="error")
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)
    

@views.route('/post_image/<filename>')
def post_image(filename):
	flash("Image successfully uploaded and displayed below", category="error")
	return redirect(url_for('static', filename= "uploads/"+filename), code=301)
    

@views.route('/like_post/<post_id>')
@login_required
def like_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    dislike=Dislike.query.filter_by(post_id=post_id,author=current_user.id).first()
    like=Like.query.filter_by(post_id=post_id,author=current_user.id).first()
    if not post:
        flash("Post not found", category="error")
    elif current_user.id == post.author:
        flash("You cannot like your own post", category="error")
    else:
            if not like :
                if not dislike:
                    lik=Like(post_id=post_id, author=current_user.id)
                    #db.session.delete(like)
                    db.session.add(lik)
                    db.session.commit()
                    return redirect(url_for("views.home"))
                else:
                    flash("You alredy dislike this post, please undislike it before like it!", category="error")
            else:
                db.session.delete(like)   
                db.session.commit()
                return redirect(url_for("views.home"))

    return redirect(url_for("views.home"))


@views.route('/dislike/<post_id>')
@login_required
def dislike_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    dislike=Dislike.query.filter_by(post_id=post_id,author=current_user.id).first()
    like=Like.query.filter_by(post_id=post_id,author=current_user.id).first()
    if not post:
        flash("Post not found", category="error")
    elif current_user.id == post.author:
        flash("You cannot like your own post", category="error")
    else:
            if not dislike:
                if not like:
                    dlik=Dislike(post_id=post_id, author=current_user.id)
                    #db.session.delete(dislike)
                    db.session.add(dlik)
                    db.session.commit()
                    return redirect(url_for("views.home"))
                else:
                    flash("You already liked this post, please unlike it before like it!", category="error")
            else:
                db.session.delete(dislike)   
                db.session.commit()
                return redirect(url_for("views.home"))

    return redirect(url_for("views.home"))
@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
