import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from flask import Blueprint, request, jsonify
from project.database.database import db
from project.database.models import MyNotes


load_dotenv(find_dotenv())
api = Blueprint('api', '__name__', url_prefix='/api/')

AUTHORIZATION_KEY = os.environ.get('AUTHORIZATION_KEY')


@api.route('/all-notes', methods=['GET', 'POST', 'DELETE'])
def all_notes():
    """Эндпоинт работы по заметкам."""

    all_notes = db.query(MyNotes).all()

    # проверка правомерности пользования API
    check = request.headers.get('Authorization', None)

    if not check or check != AUTHORIZATION_KEY:
        return {'message': 'No access'}, 405

    if request.method == 'DELETE':
        try:
            id_ = request.get_json()['id']
            db.delete(all_notes[int(id_) - 1])
            return {'message': 'Entry successfully deleted'}, 200

        except Exception as e:
            return {'message': 'Error'}, 503

    if request.method == 'POST':
        try:
            data = request.get_json()['data']
            date = datetime.now()
            new_note = MyNotes(date=date, note=data)
            db.add(new_note)
            db.commit()
            return {'message': 'Entry added successfully'}, 200
        except Exception as e:
            return jsonify({'message': 'Error'}), 503
    return jsonify({'all_notes': [i.to_dict()['note'] for i in all_notes]})
