from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
