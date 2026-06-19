from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.constants import (
    EMPTY_REQUEST_BODY_MESSAGE,
    REQUIRED_FIELD_MESSAGE,
    SHORT_NOT_FOUND_MESSAGE,
)
from yacut.models import URLMap


class InvalidAPIUsage(Exception):
    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__()
        self.message = message
        self.status_code = status_code


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify({'message': error.message}), error.status_code


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(EMPTY_REQUEST_BODY_MESSAGE)

    if 'url' not in data:
        raise InvalidAPIUsage(REQUIRED_FIELD_MESSAGE)

    try:
        url_map = URLMap.create(
            original=data['url'],
            short=data.get('custom_id'),
        )
    except ValueError as error:
        raise InvalidAPIUsage(str(error))

    return jsonify(
        {
            'url': url_map.original,
            'short_link': url_map.get_short_link(),
        }
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage(
            SHORT_NOT_FOUND_MESSAGE,
            HTTPStatus.NOT_FOUND,
        )
    return jsonify({'url': url_map.original}), HTTPStatus.OK
