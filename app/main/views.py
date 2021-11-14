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


@main.route('/posts/<username>')
@login_required
def posts(username):

    user = User.query.filter_by(username=username).first()
    if user is  None:
        flash('Username does not exist!',)
        return redirect('.index')

    posts = user.posts
    return render_template('posts.html',user=current_user,posts=posts,username=username)

@main.route('/create-comment/<post_id>', methods=['POST'])
def create_comment(post_id):

    form = CommentsForm()
    title = 'Create Comment'
    posts = Post.query.filter_by(id=post_id).first()

    if posts is None:
        abort(404)

    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(comment=comment, user_id=current_user.id,post_id=posts.id)
        new_comment.save_comment()
        return redirect(url_for('.posts', posts=posts))

    return render_template('create_comment.html',comment_form=form,title=title)
