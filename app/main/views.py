from flask import render_template
from . import main





@main.route('/')
def index():
    render_template('index.html')


@main.route('/about')
def about():
    render_template('about.html')


@main.route('/posts')
def posts():
    render_template('posts.html')

@main.route('/contact')
def contact():
    render_template('contact.html')