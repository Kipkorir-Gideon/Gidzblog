from operator import pos
from flask import render_template,request,flash,redirect,url_for,abort
from . import main
from ..models import User,Post,Comment,Like,Dislike
from .forms import PostForm,CommentsForm
from ..request import get_random_quote
from flask_login import login_required,current_user





@main.route('/')
def index():

    quote = get_random_quote()
    posts = Post.query.all()

    return render_template('index.html',quote=quote,posts=posts)


@main.route('/create-post', methods=['GET','POST'])
@login_required
def create_post():

    form = PostForm()

    if form.validate_on_submit():
        content = form.content.data

        post = Post(content=content, author=current_user.id)
        post.save_post()
        flash('Post created!', category='success')
        return redirect(url_for('.index'))

    return render_template('create_post.html',post_form=form,user=current_user)


@main.route('/posts')
def posts():
    return render_template('posts.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')