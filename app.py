from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
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


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} joined the room {}".format(data['username'], data['room']))


if __name__ == '__main__':
    socketio.run(app, debug=True)
