import minitwit
from flask import Flask, request, jsonify, g, make_response, abort
from flask_basicauth import BasicAuth
from werkzeug import check_password_hash

app = Flask('minitwit')

class DatabaseAuth(BasicAuth):
	def __init__(self, app):
		BasicAuth.__init__(self, app)

	def check_credentials(self, username, password):
		print 'Checking %s - %s' % (username, password)
		# look up username in DB
		user = minitwit.query_db('select * from user where username = ?', [username], one=True)
		if user['username'] == username and check_password_hash(user['pw_hash'], password):
		    # return True if hashed password matches password from DB
		    g.user = username
		    return True   
		else:
		    return False

auth = DatabaseAuth(app)
#app.config['BASIC_AUTH_FORCE'] = True

def populate_db():
    """Re-populates the database with test data"""
    db = minitwit.get_db()
    with app.open_resource('population.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('populatedb')
def populatedb_command():
    """Inputs data in database tables."""
    populate_db()
    print('Database population is completed.')

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized access. Username and password do not match'}), 401)


@app.errorhandler(400)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized access'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error: Method not allowed'}))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#@auth.error_handler
#def unauthorized():
#    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.route('/thread/public', methods=['GET'])
def public_thread():
    '''shows all the tweets of all users'''
    msg = minitwit.query_db('''select message.*, user.* from message, user
    where message.author_id = user.user_id
    order by message.pub_date desc limit ?''', [minitwit.PER_PAGE])
    msg = map(dict, msg)
    print msg
    return jsonify({'messages': msg})


@app.route('/home/thread/<username>', methods=['GET', 'POST'])
@auth.required
def home_timeline(username):
    """shows feed of the user and all the user is the following"""
    if(len(username) == 0):
        abort(404)

    if confirm_user(username):
        g.user = username
    else:
        abort(400)

    current_user = minitwit.query_db('select * from user where username = ?',
    [username], one=True)


    tweets = minitwit.query_db('''select message.*, user.* from message, user
        where message.author_id = user.user_id and (user.user_id = ? or user.user_id in (select whom_id from follower
                                where who_id = ?)) order by message.pub_date desc limit ?''',
                                [current_user['user_id'], current_user['user_id'], minitwit.PER_PAGE])
    tweets = map(dict, tweets)
    return jsonify(tweets)

@app.route('/thread/user/<username>', methods=['GET'])
def user_timeline(username):

    current_user = minitwit.query_db('select * from user where username = ?',
    [username], one=True)
    if current_user is None:
            abort(404)
    messages = minitwit.query_db('''
        select message.*, user.* from message, user
        where message.author_id = user.user_id and (
            user.user_id = ?)
        order by message.pub_date desc limit ?''',
        [current_user['user_id'], minitwit.PER_PAGE])
    messages = map(dict, messages)
    return jsonify({'user-messages':messages})

@app.route('/thread/user/<username>', methods=['GET', 'POST'])
def user_timeline(username):
    """shows the feed of a specific user"""

    if confirm_user(username):
        g.user = username
    else:
        abort(400)

    user = minitwit.query_db('select * from user where username = ?', [username], one=True)

    if basic_auth.check_credentials(user['username'], user['pw_hash']):
        current_user = minitwit.query_db('select * from user where username = ?',[username], one=True)
        if current_user is None:
            abort(404)
        messages = minitwit.query_db('''select message.*, user.* from message, user
        where message.author_id = user.user_id and (user.user_id = ?)
        order by message.pub_date desc limit ?''', [current_user['user_id'], minitwit.PER_PAGE])

    msg = map(dict, messages)
    return jsonify({'user-messages':msg})

@app.route('/follow/<username>/<uid>', methods=['POST', 'GET'])
def user_following(username, uid):
    '''sets the current user(username) to follow new user (uid)'''
    if(len(username) == 0) or (len(str(uid)) == 0):
        abort(404)

    if(not request.json):
        abort(405)


    info = request.get_json()
    if confirm_user(username):
        user = minitwit.query_db('select * from user where user.username = ?', [username], one=True)

    
    who_id = minitwit.get_user_id(username)
    current_user = minitwit.query_db('select * from user where username = ?',
        [username], one=True)
    db = minitwit.get_db()
    db.execute('insert into follower (who_id, whom_id) values (?, ?)', [who_id, uid])
    db.commit()
    return jsonify({'follower':current_user['username'], 'following-id': uid, 'message': 'user successfully followed'}, 201)

@app.route('/<username>/unfollow', methods=['POST', 'GET'])
@auth.required
def unfollow_user(username):
    """Removes the current user as follower of the given user."""
    if not g.user:
        abort(401)
    user = minitwit.query_db('select * from user where username = ?', [g.user], one=True)
    whom_id = minitwit.get_user_id(username)
    if whom_id is None:
        abort(404)
    db = minitwit.get_db()
    db.execute('delete from follower where who_id=? and whom_id=?',
              [user['user_id'], whom_id])
    db.commit()
    flash('You are no longer following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))



@app.route('/post_message/<int:uid>', methods=['POST', 'GET'])
def post_message(uid):
    """registers a new post/message for user."""

    if(len(str(uid)) == 0):
        abort(404)
    #check if session is valid for user
    #current_user_id = minitwit.get_user_id(username)
    if request.method == "POST":
        if(not request.json):
            abort(400)

        info = request.get_json()
        user = minitwit.query_db('select * from user where username = ?', info['username'], one=True)
        confirm_user(user['username'])


        msg = info['text']
        db = minitwit.get_db()
        db.execute('''insert into message (author_id, text, pub_date) values (?, ?, ?)''', [uid, msg, int(time.time())])
        db.commit()
        return jsonify({'user_id': uid, 'message': msg, 'time': int(time.time())}, 201)
    else:
        abort(404)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if(not request.json):
            abort(405)

        data = request.get_json()
        if not data["username"] or not data["password"] or not data["email"] or not data["password2"]:
            abort(400)
        elif data["password"] != data["password2"]:
            return jsonify({'error': 'passwords need to match'}, 406)
        else:
            '''check for duplicate user'''
            if minitwit.get_user_id(data["username"] is not None)
                return jsonify({'Error': 'user already exists'}, 406)
            else:
                db = minitwit.get_db()
                password = generate_password_hash(data['password'])
                db.execute('''insert into user (username, email, pw_hash) values (?, ?, ?)'''
                ,[data['username'], data['email'], password])
                db.commit()
                return jsonify({'message':'You have been registered in successfully','username': data['username'], 'email': data['email']}, {'Status code':201})


def confirm_user(username):
        user = minitwit.query_db('''select * from user where username = ?'''
        , [username], one=True)

        if user is None:
            return False
        else:
            app.config['BASIC_AUTH_USERNAME'] = user['username']
            app.config['BASIC_AUTH_PASSWORD'] = user['pw_hash']
            return True

if __name__ == '__main__':
    app.run(debug=True)
