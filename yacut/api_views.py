from http import HTTPStatus
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
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    # domain = urlparse(request.base_url).scheme + '://' + urlparse(request.base_url).netloc
    response_dict = url.to_dict()
    del (response_dict)['short_link']
    # response_dict['short_link'] = urlparse(request.base_url).scheme + '://' + urlparse(request.base_url).netloc + '/' + url.short
    return jsonify(response_dict), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    try:
        data = request.get_json(force=True)
    except BadRequest:
        raise InvalidAPIUsage("Отсутствует тело запроса", HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', HTTPStatus.BAD_REQUEST)
    if not is_unique(data.get('custom_id')):
        raise InvalidAPIUsage(f'Имя "{data.get("custom_id")}" уже занято.', HTTPStatus.BAD_REQUEST)
    if not latin_and_digits_length(data.get('custom_id')):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)
    url = URLMap()
    url.from_dict(data, 'url', 'custom_id')
    db.session.add(url)
    db.session.commit()
    response_dict = url.to_dict()
    response_dict['short_link'] = urlparse(request.base_url).scheme + '://' + urlparse(request.base_url).netloc + '/' + url.short
    return jsonify(response_dict), HTTPStatus.CREATED
