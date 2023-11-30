from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_cors import CORS
from ftpService import FtpService
from dbService import DatabaseService
import os
import sys
import base64

load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from application import create_app

# app/sockets
app = create_app()
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# database
db = SQLAlchemy(app)
ftp_service = FtpService()
data_service = DatabaseService(db, ftp_service)


def broadcast_add(new_event):
    socketio.emit('add_event', new_event)


def broadcast_delete(event_id):
    socketio.emit('delete_event', event_id)


@socketio.on('message')
def handle_message(msg):
    print('Received message: ', msg)
    socketio.emit('message', msg)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Urban Guard</h1>"


@app.route('/api/event', methods=['POST'])
def post_event():
    try:
        form = request.form
        try:
            file = request.files['file']
        except Exception as e:
            print(f"Upload file Error: {e}")
            return jsonify({'status': 'error', 'message': "Не удалось получить данные о файле"})

        new_event = data_service.add_event(form, file)
        broadcast_add(new_event)
        return jsonify({'status': 'success', 'message': 'Данные получены'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/api/events', methods=['GET'])
def get_xyi():
    try:
        events_data = data_service.get_all()
        return jsonify({'status': 'success', 'message': 'Данные получены', 'events': events_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/api/delete/last', methods=['DELETE'])
def delete_last_post():
    try:
        event_id = data_service.delete_last()
        broadcast_delete(event_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/api/file/file_id', methods=['GET', 'POST'])
def get_file(file_id):
    try:
        file_info = ftp_service.get_file(file_id)
        file_data_base64 = base64.b64encode(file_info["file_data"]).decode('utf-8')
        response_data = {"status": "success", "event_id": file_id, "remote_path": file_info["remote_path"], "file_data": file_data_base64}
        return response_data
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug=True)

