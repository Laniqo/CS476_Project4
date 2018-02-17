import minitwit
from flask import Flask, request, jsonify, g, make_response
from flask_basicauth import BasicAuth

app = Flask('minitwit')

auth = BasicAuth(app)
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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.route('/thread/public', methods=['GET'])
def public_thread():
    '''shows all the tweets of all users'''
    msg = minitwit.query_db('''select message.*, user.* from message, user
    where message.author_id = user.user_id
    order by message.pub_date desc limit ?''', [minitwit.PER_PAGE])
    msg = map(dict, msg)
    print msg
    return jsonify({'messages': msg})


@app.route('/thread/home', methods=['GET'])
def home_timeline():
    """shows feed of the user and all the user is the following"""
    if not g.user:
        return abort(403)

    msg = minitwit.query_db('''select message.*, user.* from message, user
    where message.author_id = user.user_id and (
        user.user_id = ? or
        user.user_id in (select whom_id from follower
                                where who_id = ?))
    order by message.pub_date desc limit ?''',
    [session['user_id'], session['user_id'], PER_PAGE])
    print tweets
    tweets = map(dict, tweets)
    print tweets
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

@app.route('/post', methods=['POST'])
def post_message():
    """registers a new post/message for user."""
    #check if session is valid for user
    if request.method == "POST":
        json_dict = request.get_json()

        msg = json_dict['text']
        return jsonify({'message': msg})

    #add http status code 201 for successfully accepted

@app.route('/sample', methods=['GET'])
def get_name():
    """sample to get user name"""
    return jsonify({'name': auth.username()})

"""@app.route('/<username>/follow', methods=['POST'])
def user_following(username):
    #gets all the users the user is follwoing
    current_user = minitwit.query_db('select user_id from user where username = ?',
    [username], one=True)
    following = minitwit.query_db('''select * from follower where following) """

    #check_credential when user logs in and then uses init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
