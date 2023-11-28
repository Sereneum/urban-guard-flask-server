from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request
from ftpService import FtpService
from dbService import DatabaseService
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from application import create_app

app = create_app()
db = SQLAlchemy(app)
ftp_service = FtpService()
data_service = DatabaseService(db, ftp_service)


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

        data_service.add_event(form, file)

        return jsonify({'status': 'success', 'message': 'Данные получены'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        events_data = data_service.get_all()
        return jsonify({'status': 'success', 'message': 'Данные получены', 'events': events_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == "__main__":
    app.run()

