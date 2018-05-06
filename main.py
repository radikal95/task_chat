from flask import Flask
from flask_socketio import SocketIO,send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

@socketio.on('messege')
def handleMessege(msg):
    print('Messege: ' + msg)

if __name__ == '__main__':
    socketio.run(app)

