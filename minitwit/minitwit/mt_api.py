import minitwit
import time
import uuid
import os
import string
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, jsonify, g, make_response, abort, _app_ctx_stack
from flask_basicauth import BasicAuth
from werkzeug import check_password_hash, generate_password_hash
from sqlite3 import OperationalError

#configuration
app = Flask(__name__)
#DATABASE = 'database.db'
DATABASE1 = 'database1.db'
DATABASE2 = 'database2.db'
DATABASE3 = 'database3.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

NUMOFSERVERS = 3;
DATABASES = []

f = os.path.join(app.root_path, DATABASE1)
DATABASES.append(DATABASE1)
f = os.path.join(app.root_path, DATABASE2)
DATABASES.append(DATABASE2)
f = os.path.join(app.root_path, DATABASE3)
DATABASES.append(DATABASE3)

app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

#DATABASE = os.path.join(app.root_path, 'database.db')


#for filename in os.listdir(app.root_path):
#    f = os.path.join(DIRECTORY,filename)
#    DATABASES.append(f)

def query_db(database, query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db(database).execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def query_all_db(query, args=(), one=False):
    ret = []
    print query
    for database in DATABASES:
        try:
            cur = get_db(database).execute(query, args)
            for row in cur.fetchall():
                print "-- values: %s" % (row)
                ret.append(row)
        except sqlite3.Error, err:
            print "[Error] %s" %err

    return (ret[0] if ret else None) if one else ret


#pass the Database 1 2 or 3
def get_db(database):
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top

    if not hasattr(top, 'sqlite_db1') and database == DATABASE1:
        top.sqlite_db1 = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        top.sqlite_db1.row_factory = sqlite3.Row
    if not hasattr(top, 'sqlite_db2') and database == DATABASE2:
        top.sqlite_db2 = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        top.sqlite_db2.row_factory = sqlite3.Row
    if not hasattr(top, 'sqlite_db3') and database == DATABASE3:
        top.sqlite_db3 = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        top.sqlite_db3.row_factory = sqlite3.Row

    if database == DATABASE1:
        return top.sqlite_db1
    if database == DATABASE2:
        return top.sqlite_db2
    if database == DATABASE3:
        return top.sqlite_db3


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db1'):
        top.sqlite_db1.close()
    if hasattr(top, 'sqlite_db2'):
        top.sqlite_db2.close()
    if hasattr(top, 'sqlite_db3'):
        top.sqlite_db3.close()


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


def get_server_number(uid):
    str_uid = str(uid)
    result = (uuid.UUID(str_uid).int % NUMOFSERVERS)
    return result

def populate_db():
    #Populates the database.
    #db = get_db()
    queries = []

    fd1 = open('population.sql', 'r')
    populate1 = fd1.read()
    queries.append(populate1)
    fd1.close();

    fd2 = open('population2.sql', 'r')
    populate2 = fd2.read()
    queries.append(populate2)
    fd2.close();

    fd3 = open('population3.sql', 'r')
    populate3 = fd3.read()
    queries.append(populate3)
    fd3.close();

    counter = 0

    for query in queries:
        sqlCommands = query.split(';')
        for command in sqlCommands:
            try:
                if command.find('?') != -1:
                    uid = uuid.uuid4()
                    str_uid = str(uid)
                    command = command.replace('?', str_uid, 1 )
                    db_number = get_server_number(uid)
                    db = get_db(DATABASES[db_number])
                    db.cursor().execute(command)
                    db.commit()
                else:
                    db = get_db(DATABASES[counter])
                    db.cursor().execute(command)
                    db. commit()
            except OperationalError, msg:
                print "Command skipped: ", msg
        counter+=1


def init_db():
    """Initializes the database."""
    #db = get_db()
    #with app.open_resource('schema.sql', mode='r') as f:
    #    db.cursor().executescript(f.read())
    #db.commit()
    schema = open('schema.sql', 'r')
    schema_commands = schema.read()
    schema.close();

    sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))

    for database in DATABASES:
        try:
            db = get_db(database)
            db.cursor().executescript(schema_commands)
            db.commit()
        except sqlite3.Error, err:
            print " [INFO] %s " % err

    #with sqlite3.connect(DATABASES[0], detect_types=sqlite3.PARSE_DECLTYPES) as conn:
    #    conn.text_factory = str
    #    cur = conn.cursor()
    #    cur.executescript(schema_commands)

    #with sqlite3.connect(DATABASES[1], detect_types=sqlite3.PARSE_DECLTYPES) as conn:
    #    conn.text_factory = str
    #    cur = conn.cursor()
    #    cur.executescript(schema_commands)

    #with sqlite3.connect(DATABASES[2], detect_types=sqlite3.PARSE_DECLTYPES) as conn:
    #    conn.text_factory = str
    #    cur = conn.cursor()
    #    cur.executescript(schema_commands)


class DatabaseAuth(BasicAuth):
    def __init__(self, app):
        BasicAuth.__init__(self, app)

    def check_credentials(self, username, password):
        print 'Checking %s - %s' % (username, password)
		# look up username in DB
        user = query_all_db('select * from user where username = ?', [username], one=True)

        if user is None:
            abort(make_response(jsonify(message="User does not exist"),401))
        if user['username'] == username and check_password_hash(user['pw_hash'], password):
		    # return True if hashed password matches password from DD
            server_num = get_server_number(user['user_id'])
            g.user = query_db(DATABASES[server_num], 'select * from user where username = ?',[username], one=True)
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
    rv = query_all_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None

def get_user_name(user_id):
    """Convenience method to look up the id for a username."""
    server_num = get_server_number(user_id)
    rv = query_db(DATABASES[server_num], 'select username from user where user_id = ?',
                  uuid.UUID([user_id]), one=True)
    return rv[0] if rv else None


#added this for the timeline page to check if current user is following
#the user of the current profile being viewed
@app.route('/followed/<user_id>/<profile_id>', methods=['GET', 'POST'])
def followed(user_id, profile_id):
    json_object = request.get_json()
    server_num = get_server_number(json_object['user_id'])
    followed = query_db( DATABASES[server_num],'''select 1 from follower where
        follower.who_id = ? and follower.whom_id = ?''',
        [json_object['user_id'], json_object['profile_id']], one=True ) is not None

    return jsonify(followed)


#helper functions that grab the user's info by user_id or username
@app.route('/user_info/<user_id>', methods=['GET', 'POST'])
def user_info(user_id):
    json_object = request.get_json()
    server_num = get_server_number(json_object['user_id'])

    user = query_db( DATABASES[server_num], 'select * from user where user_id = ?', [json_object['user_id']], one=True)
    if user is None:
        abort(404)
    user = dict(user)
    return jsonify(user);

@app.route('/confirm_username/<username>', methods=['GET', 'POST'])
def confirm_username(username):
    json_object = request.get_json()
    user = query_all_db('select * from user where username = ?', [json_object['username']], one=True)

    if user is None:
        abort(404)

    user = dict(user)
    return jsonify(user);

@app.route('/posts/public', methods=['GET'])
def public_thread():
    '''Returns all the posted msgs of all users'''
    msg = query_all_db('''select message.*, user.user_id, user.username, user.email from message, user
    where message.author_id = user.user_id
    order by message.pub_date desc limit ?''', [PER_PAGE])

    msg = map(dict, msg)
    msg = sorted(msg, key=lambda msg: msg['pub_date'], reverse=True)
    return jsonify(msg)


@app.route('/home', methods=['GET'])
def home_timeline():
    """Shows feed of the current user and all the user is following. If no user is logged in, redirect to public page"""

    json_object = request.get_json()

    msg = query_all_db('''select message.*, user.user_id, user.username, user.email from message, user
        where message.author_id = user.user_id and (user.user_id = ? or user.user_id in (select whom_id from follower
                                where who_id = ?)) order by message.pub_date desc limit ?''',
                                [json_object['user_id'], json_object['user_id'], PER_PAGE])

    msg = map(dict, msg)
    msg = sorted(msg, key=lambda msg: msg['pub_date'], reverse=True)

    return jsonify(msg)


@app.route('/posts/<username>', methods=['GET'])
def user_timeline(username):
    """Returns the messages/posts of a specific user"""
    if(len(username) == 0):
        abort(404)
    
    json_object = request.get_json()
    uid = get_user_id(json_object['username'])
    server_num = get_server_number(uid)
    messages = query_db( DATABASES[server_num], '''select message.*, user.* from message, user
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

    server_num = get_server_number(who_id)
    db = get_db(DATABASES[server_num])
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

    server_num = get_server_number(who_id)
    db = get_db(DATABASES[server_num])
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

        server_num = get_server_number(json_object['user_id'])
        db = get_db(DATABASES[server_num])
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
                uid = uuid.uuid4()
                server_num = get_server_number(uid)
                db = get_db(DATABASES[server_num])
                password = generate_password_hash(data['password'])
                db.execute('''insert into user (user_id, username, email, pw_hash) values (?, ?, ?, ?)'''
                ,[uid, data['username'], data['email'], password])
                db.commit()
                return jsonify({'username': data['username'], 'email': data['email'], 'status': 'Successfully registered.', 'status code':201})


if __name__ == '__main__':
    app.run(debug=True)
