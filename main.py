from flask import Flask, request, jsonify
from dbService import DatabaseService
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from ftpService import FtpService
load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URL')
db = SQLAlchemy(app)
ftp_service = FtpService()
data_service = DatabaseService(db, ftp_service)


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
        # events_data = jsonify({data_service.get_all()})
        return jsonify({'status': 'success', 'message': 'Данные получены', 'events': events_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
