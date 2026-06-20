from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap


EMPTY_REQUEST_BODY_MESSAGE = 'Отсутствует тело запроса'
REQUIRED_FIELD_MESSAGE = '"url" является обязательным полем!'
SHORT_NOT_FOUND_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(EMPTY_REQUEST_BODY_MESSAGE)

    if 'url' not in data:
        raise InvalidAPIUsage(REQUIRED_FIELD_MESSAGE)

    try:
        return jsonify(
            {
                'url': data['url'],
                'short_link': URLMap.create(
                    original=data['url'],
                    short=data.get('custom_id'),
                ).get_short_link(),
            }
        ), HTTPStatus.CREATED
    except ValueError as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage(
            SHORT_NOT_FOUND_MESSAGE,
            HTTPStatus.NOT_FOUND,
        )
    return jsonify({'url': url_map.original}), HTTPStatus.OK
