from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room
import logging

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/chat')
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


if __name__ == '__main__':
    socketio.run(app, debug=True)
