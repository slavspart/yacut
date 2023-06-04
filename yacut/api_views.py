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
