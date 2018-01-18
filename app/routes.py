from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)

from flask_login import current_user, login_user, logout_user

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

from werkzeug.urls import url_parse #To verify that the next page is a relative link
from app.models import User # To do querys
from flask import request # to Allow looking at request variables

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flast('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')# this pulls the arguments from the request (?=next)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))

        return redirect(url_for('index'))

    return render_template('login.html',  title='Sign In', form=form)
