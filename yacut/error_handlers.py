from http import HTTPStatus

from flask import jsonify, render_template

from yacut import app


PAGE_NOT_FOUND_MESSAGE = 'Страница не найдена'
INTERNAL_SERVER_ERROR_MESSAGE = 'Внутренняя ошибка сервера'


class InvalidAPIUsage(Exception):
    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__()
        self.message = message
        self.status_code = status_code


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify({'message': error.message}), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return (
        render_template('error.html', message=PAGE_NOT_FOUND_MESSAGE),
        HTTPStatus.NOT_FOUND,
    )


@app.errorhandler(500)
def internal_server_error(error):
    return (
        render_template('error.html', message=INTERNAL_SERVER_ERROR_MESSAGE),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
