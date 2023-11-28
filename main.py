from flask import Flask, request, jsonify
from dbService import DatabaseService
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from ftpService import FtpService
load_dotenv()

# POSTGRES_URL = os.getenv('POSTGRES_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URL')
db = SQLAlchemy(app)
ftp_service = FtpService()
data_service = DatabaseService(db, ftp_service)


@app.route('/api/event', methods=['POST'])
def event():
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


if __name__ == '__main__':
    app.run(debug=True)
