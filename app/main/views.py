from flask import render_template,request,redirect,url_for,abort
from . import main
from ..request import get_random_quote





@main.route('/')
def index():

    quote = get_random_quote('quote')
    author = get_random_quote('author')

    return render_template('index.html',quote=quote,author=author)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/posts')
def posts():
    return render_template('posts.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')