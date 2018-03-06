import minitwit
import time
from flask import Flask, request, jsonify, g, make_response, abort
from flask_basicauth import BasicAuth
from werkzeug import check_password_hash, generate_password_hash
from sqlite3 import OperationalError

app = Flask(__name__)

class DatabaseAuth(BasicAuth):
	def __init__(self, app):
		BasicAuth.__init__(self, app)

	def check_credentials(self, username, password):
		print 'Checking %s - %s' % (username, password)
		# look up username in DB
		user = minitwit.query_db('select * from user where username = ?', [username], one=True)

		if user is None:
			abort(make_response(jsonify(message="User does not exist"),401))

		if user['username'] == username and check_password_hash(user['pw_hash'], password):
		    # return True if hashed password matches password from DB
		    g.user = minitwit.query_db('select * from user where username = ?',
                              [username], one=True)
		    return True
		else:
			return False
		    #abort(make_response(jsonify(message="Unauthorized access. Correct username and password required"), 401))

auth = DatabaseAuth(app)


def populate_db():
    #Populates the database.
    db = minitwit.get_db()
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


@app.cli.command('populatedb')
def populatedb_command():
    """Inputs data in database tables."""
    populate_db()
    print('Database population is completed.')

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


@app.route('/posts/public', methods=['GET'])
def public_thread():
    '''Returns all the posted msgs of all users'''
    msg = minitwit.query_db('''select message.*, user.user_id, user.username, user.email from message, user
    where message.author_id = user.user_id
    order by message.pub_date desc limit ?''', [minitwit.PER_PAGE])
    msg = map(dict, msg)
    return jsonify(msg)

@app.route('/home', methods=['GET'])
@auth.required
def home_timeline():
    """Shows feed of the current user and all the user is following. If no user is logged in, redirect to public page"""
    if not g.user:
        abort(401)

    msg = minitwit.query_db('''select message.*, user.user_id, user.username, user.email from message, user
        where message.author_id = user.user_id and (user.user_id = ? or user.user_id in (select whom_id from follower
                                where who_id = ?)) order by message.pub_date desc limit ?''',
                                [g.user['user_id'], g.user['user_id'], minitwit.PER_PAGE])
    msg = map(dict, msg)
    return jsonify(msg)


@app.route('/posts/<username>', methods=['GET'])
@auth.required
def user_timeline(username):
    """Returns the messages/posts of a specific user"""
    if(len(username) == 0):
        abort(404)
    if not g.user:
		abort(401)

    messages = minitwit.query_db('''select message.*, user.username, user.user_id from message, user
        where message.author_id = user.user_id and (user.user_id = ?)
        order by message.pub_date desc limit ?''', [g.user['user_id'], minitwit.PER_PAGE])

    msg = map(dict, messages)
    return jsonify(msg)

@app.route('/follow/<username>', methods=['PUT', 'GET'])
@auth.required
def user_following(username):
    '''sets the current user(username) to follow new user (uid)'''
    if(len(username) == 0):
        abort(404)
    if not g.user:
		abort(401)
	if request.method == "PUT":
        if(not request.json):
            abort(405)

    info = request.get_json()

    whom_id = minitwit.get_user_id(username)
    if whom_id is None:
		abort(404)

    db = minitwit.get_db()
    db.execute('insert into follower (who_id, whom_id) values (?, ?)', [g.user['user_id'],whom_id])
    db.commit()
    return jsonify({'follower':g.user['username'], 'following': username, 'Message': 'User successfully followed', 'Status code':201})

@app.route('/unfollow/<username>', methods=['DELETE', 'GET'])
@auth.required
def unfollow_user(username):
    """Removes the current user as a follower of the given username parameter."""
    if not g.user:
        abort(401)   
    if request.method == "DELETE":
       if(not request.json):
            abort(400)    
    whom_id = minitwit.get_user_id(username)
    if whom_id is None:
        abort(404)
       
    db = minitwit.get_db()
    db.execute('delete from follower where who_id=? and whom_id=?',
              [user['user_id'], whom_id])
    db.commit()
    return jsonify({'follower':g.user['username'], 'unfollowed': username, 'Message': 'User successfully unfollowed','Status code':201})


@app.route('/post_message', methods=['POST', 'GET'])
@auth.required
def post_message():
    """registers a new post/message for current user."""
    if not g.user:
		abort(401)
    if request.method == "POST":
        if(not request.json):
            abort(400)

        info = request.get_json()
        msg = info['text'] #gets the message that user wants to post

        db = minitwit.get_db()
        db.execute('''insert into message (author_id, text, pub_date) values (?, ?, ?)''', [g.user['user_id'], msg, int(time.time())])
        db.commit()

        return jsonify({'username': g.user['username'], 'message': msg, 'time': int(time.time()), 'status' : 'message successfully added', 'Status code':201})

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
            if minitwit.get_user_id(data["username"]) is not None:
                abort(make_response(jsonify({'Error': "User already exists"}), 406))
            else:
                db = minitwit.get_db()
                password = generate_password_hash(data['password'])
                db.execute('''insert into user (username, email, pw_hash) values (?, ?, ?)'''
                ,[data['username'], data['email'], password])
                db.commit()
                return jsonify({'username': data['username'], 'email': data['email'], 'status': 'Successfully registered.', 'status code':201})


if __name__ == '__main__':
    app.run(debug=True)
