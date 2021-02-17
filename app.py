from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from bson.json_util import dumps
from pymongo.errors import DuplicateKeyError

from db import save_user, get_user, save_room, add_room_members, get_room, get_room_members, get_rooms_for_user, \
    is_room_member, is_room_admin, update_room, remove_room_members

app = Flask(__name__)
app.secret_key = 'cokgizli'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)
        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = 'Failed to login!'

    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            save_user(username, email, password)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists!"
    return render_template('signup.html', message=message)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create_room/', methods=['GET', 'POST'])
@login_required
def create_room():
    message = ''
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip()
                     for username in request.form.get('members').split(',')]

        if len(room_name) and len(usernames):
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames,
                             current_user.username)
        else:
            message = "Failed to create room"

    return render_template('create_room.html', message=message)


@app.route('/chat')
@login_required
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('index'))


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} sent message to the room {}: {}".format(
        data['username'], data['room'], data['message']))
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} joined the room {}".format(
        data['username'], data['room']))
    join_room(data['room'])
    """ This function puts the user in a room, under the current namespace.
    This is a function that can only be called from a SocketIO event handler. """
    socketio.emit('join_room_announcement', data)


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == '__main__':
    socketio.run(app, debug=True)
