# -*- coding: utf-8 -*-
"""
    MiniTwit
    ~~~~~~~~

    A microblogging application written with Flask and sqlite3.

    :copyright: © 2010 by the Pallets team.
    :license: BSD, see LICENSE for more details.
"""

import time
import requests
import mt_api
from sqlite3 import OperationalError
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

app = Flask('minitwit')
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

#MT_API URL Config *******this will change to port 8080 for nginx back end ********
URL = 'http://localhost:5101/'

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'https://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        payload = {'user_id': session['user_id']}
        r = requests.get(URL + 'user_info/' + str(session['user_id']), json=payload)
        g.user = r.json()

@app.route('/')
def timeline():
    """Shows a users timeline or if no user is logged in it will
    redirect to the public timeline.  This timeline shows the user's
    messages as well as all the messages of followed users.
    """
    if not g.user:
        return redirect(url_for('public_timeline'))

    payload = {'user_id': session['user_id']}

    r = requests.get(URL + 'home', json=payload)

    return render_template('timeline.html', messages=r.json())


@app.route('/public')
def public_timeline():
    """Displays the latest messages of all users."""
    payload = {}
    r = requests.get(URL + 'posts/public', json = payload)
    return render_template('timeline.html', messages=r.json())


@app.route('/<username>')
def user_timeline(username):
    """Display's a users tweets."""

    #grab the current profile's info
    payload={'username': username}

    r = requests.get(URL + 'confirm_username/'+ str(username), json=payload)

    profile_user = r.json()

    if profile_user is None:
        abort(404)

    followed = False
    if g.user:
        payload = {'user_id': session['user_id'], 'profile_id': profile_user['user_id']}
        r = requests.get(URL + 'followed/'+ str(session['user_id']) + '/' + str(profile_user['user_id']), json = payload)
        followed = r.json()

    payload={'username': username}
    r = requests.get(URL + 'posts/' + str(username), json=payload)

    return render_template('timeline.html', messages=r.json(), followed=followed,
            profile_user=profile_user)


@app.route('/<username>/follow', methods=['PUT', 'POST'])
def follow_user(username):
    """Adds the current user as follower of the given user."""
    if not g.user:
        abort(401)

    payload = {'current_user' : session['user_id'], 'profile_user': username}
    r = requests.post(URL + str(username) + '/follow', json=payload)

    flash('You are now following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))


@app.route('/<username>/unfollow',methods=['PUT', 'DELETE'])
def unfollow_user(username):
    """Removes the current user as follower of the given user."""
    if not g.user:
        abort(401)

    payload = {'current_user' : session['user_id'], 'profile_user': username}
    r = requests.delete(URL + str(username) + '/unfollow', json=payload)

    flash('You are no longer following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))


@app.route('/add_message', methods=['POST', 'GET'])
def add_message():
    """Registers a new message for the user."""
    if 'user_id' not in session:
        abort(401)

    if request.method == 'POST':
        print 'LINE 135 ********** THIS EXECUTED'
        payload = {'user_id': session['user_id'], 'text': request.form['text']}
        r = requests.post(URL + 'post_message', json= payload, stream=True)
        #print str(r.json())
        if r.status_code == 200:
            flash('Your message was recorded')
            return redirect(url_for('timeline'))

    return redirect(url_for('timeline'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""

    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        payload={'username':request.form['username']}
        username = request.form['username']
        r = requests.get(URL + 'confirm_username/' + str(username), json=payload)

        user = r.json()
        print 'USER is %r' % user
        print 'FORM is %r' % request.form
        if user is None:
            error = 'Invalid username'
        elif 'error' in user:
            error = user['error']
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(url_for('timeline'))

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""

    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif mt_api.get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            payload = {'username' : request.form['username'], 'email': request.form['email'],
            'password': request.form['password'],'password2': request.form['password2']}

            r = requests.post(URL + 'register', json= payload)
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('public_timeline'))


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url
