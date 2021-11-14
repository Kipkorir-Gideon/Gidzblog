from operator import pos
from flask import render_template,request,flash,redirect,url_for,abort
from . import main
from .. import db,photos
from ..models import User,Post,Comment,Like,Dislike
from .forms import PostForm,CommentsForm,UpdateProfile
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


@main.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if post is  None:
        abort(404)

    elif current_user.id != post.id:
        flash('You do not have permission to delete this post!')

    else:
        delete_post()
        flash('Post deleted successfully!')

    return redirect(url_for('.index'))



@main.route('/delete-comment/<id>')
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()

    if comment is None:
        flash('Comment not found!')

    elif current_user.id != comment.user_id and current_user.id != comment.post.user_id:
        flash('You are not allowed to delete this comment!')

    else:
        delete_comment()

    return redirect(url_for('.index'))


@main.route('like-post<post_id>', methods=['GET','POST'])
@login_required
def like_post(id):
    get_posts = Like.get_likes(id)
    valid_string = f'{current_user.id}:{id}'
    for post in get_posts:
        to_str = f'{post}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('.posts',id=id))
        else:
            continue
    like = Like(user = current_user, post_id=id)
    like.save_likes()
    return redirect(url_for('.posts',id=id))


@main.route('/dislike-post<post_id>', methods=['GET','POST'])
@login_required
def dislike_post(id):
    get_posts = Dislike.get_dislikes(id)
    valid_string = f'{current_user.id}:{id}'
    for post in get_posts:
        to_str = f'{post}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('.posts',id=id))
        else:
            continue
    dislike = Dislike(user = current_user, post_id=id)
    dislike.save_dislikes()
    return redirect(url_for('.posts',id=id))


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))