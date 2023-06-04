from urllib.parse import urlparse

from werkzeug.exceptions import BadRequest
from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validators import latin_and_digits_length, is_unique


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    url = URLMap.query.filter_by(short=short).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    # domain = urlparse(request.base_url).scheme + '://' + urlparse(request.base_url).netloc
    response_dict = url.to_dict()
    del (response_dict)['short_link']
    # response_dict['short_link'] = urlparse(request.base_url).scheme + '://' + urlparse(request.base_url).netloc + '/' + url.short
    return jsonify(response_dict), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    try:
        data = request.get_json(force=True)
    except BadRequest:
        raise InvalidAPIUsage("Отсутствует тело запроса", 400)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)
    if not is_unique(data.get('custom_id')):
        raise InvalidAPIUsage(f'Имя "{data.get("custom_id")}" уже занято.', 400)
    if not latin_and_digits_length(data.get('custom_id')):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    url = URLMap()
    url.from_dict(data, 'url', 'custom_id')
    db.session.add(url)
    db.session.commit()
    response_dict = url.to_dict()
    response_dict['short_link'] = urlparse(request.base_url).scheme + '://' + urlparse(request.base_url).netloc + '/' + url.short
    return jsonify(response_dict), 201


# def update_opinion(id):
#     data = request.get_json(force=True)
#     if (
#         'text' in data and
#         Opinion.query.filter_by(text=data['text']).first() is not None
#     ):
#         raise InvalidAPIUsage('Такое мнение уже есть в базе данных')
#     opinion = Opinion.query.get(id)
#     # Тут код ответа нужно указать явным образом
#     if opinion is None:
#         raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
#     opinion.title = data.get('title', opinion.title)
#     opinion.text = data.get('text', opinion.text)
#     opinion.source = data.get('source', opinion.source)
#     opinion.added_by = data.get('added_by', opinion.added_by)
#     db.session.commit()
#     return jsonify({'opinion': opinion.to_dict()}), 201


# @app.route('/api/opinions/<int:id>/', methods=['DELETE'])
# def delete_opinion(id):
#     opinion = Opinion.query.get(id)
#     if opinion is None:
#         # Тут код ответа нужно указать явным образом
#         raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
#     db.session.delete(opinion)
#     db.session.commit()
#     return '', 204

# @app.route('/api/opinions/', methods=['GET'])
# def get_opinions():
#     # Запрашивается список объектов
#     opinions = Opinion.query.all()
#     # Поочерёдно сериализуется каждый объект,
#     # а потом все объекты помещаются в список opinions_list
#     opinions_list = [opinion.to_dict() for opinion in opinions]
#     return jsonify({'opinions': opinions_list}), 200
