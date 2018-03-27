import minitwit
import time
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, jsonify, g, make_response, abort, _app_ctx_stack
from flask_basicauth import BasicAuth
from werkzeug import check_password_hash, generate_password_hash
from sqlite3 import OperationalError

#configuration
DATABASE = 'database.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


@app.cli.command('populatedb')
def populatedb_command():
    """Inputs data in database tables."""
    populate_db()
    print('Database population is completed.')


def populate_db():
    #Populates the database.
    db = get_db()
    fd = open('population.sql', 'r')
    populate = fd.read()
    fd.close();

    sqlCommands = populate.split(';')

    for command in sqlCommands:
        try:
            db.cursor().execute(command)
            db.commit()
        except OperationalError, msg:
            print "Command skipped: ", msg


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


class DatabaseAuth(BasicAuth):
	def __init__(self, app):
		BasicAuth.__init__(self, app)

	def check_credentials(self, username, password):
		print 'Checking %s - %s' % (username, password)
		# look up username in DB
		user = query_db('select * from user where username = ?', [username], one=True)

		if user is None:
			abort(make_response(jsonify(message="User does not exist"),401))

		if user['username'] == username and check_password_hash(user['pw_hash'], password):
		    # return True if hashed password matches password from DB
		    g.user = query_db('select * from user where username = ?',
                              [username], one=True)
		    return True
		else:
			return False
		    #abort(make_response(jsonify(message="Unauthorized access. Correct username and password required"), 401))

auth = DatabaseAuth(app)

"""Error messages Jsonified"""
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized access. Incorrect email and address entered'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}, 405))

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None

def get_user_name(user_id):
    """Convenience method to look up the id for a username."""
    rv = query_db('select username from user where user_id = ?',
                  [user_id], one=True)
    return rv[0] if rv else None


#added this for the timeline page to check if current user is following
#the user of the current profile being viewed
@app.route('/followed/<user_id>/<profile_id>', methods=['GET', 'POST'])
def followed(user_id, profile_id):
    json_object = request.get_json()
    followed = query_db('''select 1 from follower where
        follower.who_id = ? and follower.whom_id = ?''',
        [json_object['user_id'], json_object['profile_id']], one=True) is not None

    return jsonify(followed)


#helper functions that grab the user's info by user_id or username
@app.route('/user_info/<user_id>', methods=['GET', 'POST'])
def user_info(user_id):
    json_object = request.get_json()
    user = query_db('select * from user where user_id = ?', [json_object['user_id']], one=True)
    if user is None:
        abort(404)
    user = dict(user)
    return jsonify(user);

@app.route('/confirm_username/<username>', methods=['GET', 'POST'])
def confirm_username(username):
    json_object = request.get_json()
    user = query_db('select * from user where username = ?', [json_object['username']], one=True)
    if user is None:
        abort(404)

    user = dict(user)

    return jsonify(user);

@app.route('/posts/public', methods=['GET'])
def public_thread():
    '''Returns all the posted msgs of all users'''
    msg = query_db('''select message.*, user.user_id, user.username, user.email from message, user
    where message.author_id = user.user_id
    order by message.pub_date desc limit ?''', [PER_PAGE])
    msg = map(dict, msg)
    return jsonify(msg)


@app.route('/home', methods=['GET'])
def home_timeline():
    """Shows feed of the current user and all the user is following. If no user is logged in, redirect to public page"""

    json_object = request.get_json()

    msg = query_db('''select message.*, user.user_id, user.username, user.email from message, user
        where message.author_id = user.user_id and (user.user_id = ? or user.user_id in (select whom_id from follower
                                where who_id = ?)) order by message.pub_date desc limit ?''',
                                [json_object['user_id'], json_object['user_id'], PER_PAGE])
    msg = map(dict, msg)

    return jsonify(msg)


@app.route('/posts/<username>', methods=['GET'])
def user_timeline(username):
    """Returns the messages/posts of a specific user"""
    if(len(username) == 0):
        abort(404)
    #if not g.user:
	#	abort(401)
    json_object = request.get_json()
    uid = get_user_id(json_object['username'])
    messages = query_db('''select message.*, user.* from message, user
        where message.author_id = user.user_id and (user.user_id = ?)
        order by message.pub_date desc limit ?''', [uid, PER_PAGE])

    msg = map(dict, messages)

    return jsonify(msg)

@app.route('/<username>/follow', methods=['PUT', 'POST', 'GET'])
@auth.required
def follow_user(username):
    '''sets the current user(username) to follow new user (uid)'''
    if(len(username) == 0):
        abort(404)
    if not g.user:
		abort(401)
    if request.method == "POST":
        if(not request.json):
            abort(405)

    json_object = request.get_json()

    whom_id = get_user_id(json_object['profile_user'])
    if whom_id is None:
		abort(404)

    who_id = json_object['current_user']
    if who_id is None:
    	abort(404)

    db = get_db()
    db.execute('insert into follower (who_id, whom_id) values (?, ?)', [who_id,whom_id])
    db.commit()

    return jsonify(json_object)

@app.route('/<username>/unfollow', methods=['DELETE', 'GET'])
@auth.required
def unfollow_user(username):
    """Removes the current user as a follower of the given username parameter."""
    if not g.user:
        abort(401)

    if request.method == "DELETE":
       if(not request.json):
            abort(400)

    json_object = request.get_json()
    whom_id = get_user_id(json_object['profile_user'])
    if whom_id is None:
        abort(404)

    who_id = json_object['current_user']
    if who_id is None:
        abort(404)

    db = get_db()
    db.execute('delete from follower where who_id=? and whom_id=?',
              [who_id, whom_id])
    db.commit()
    return jsonify(json_object)


@app.route('/post_message', methods=['POST', 'GET'])
@auth.required
def post_message():
    """registers a new post/message for current user."""
    if not g.user:
		abort(401)
    if request.method == "POST":
        if(not request.json):
            abort(400)

        json_object = request.get_json()
        text = json_object['text']

        db = get_db()
        db.execute('''insert into message (author_id, text, pub_date) values (?, ?, ?)''', [json_object['user_id'], text, int(time.time())])
        db.commit()

        return jsonify(json_object)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if(not request.json):
            abort(405)

        data = request.get_json()

        if not data["username"] or not data["password"] or not data["email"] or not data["password2"]:
            abort(make_response(jsonify({'Error': "Please enter correct information"}), 402))
        elif data["password"] != data["password2"]:
            abort(make_response(jsonify({'Error': "Passwords need to match"}), 402))
        else:
            '''check for duplicate user'''
            if get_user_id(data["username"]) is not None:
                abort(make_response(jsonify({'Error': "User already exists"}), 406))
            else:
                db = get_db()
                password = generate_password_hash(data['password'])
                db.execute('''insert into user (username, email, pw_hash) values (?, ?, ?)'''
                ,[data['username'], data['email'], password])
                db.commit()
                return jsonify({'username': data['username'], 'email': data['email'], 'status': 'Successfully registered.', 'status code':201})


if __name__ == '__main__':
    app.run(debug=True)
