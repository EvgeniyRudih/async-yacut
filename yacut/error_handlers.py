from http import HTTPStatus

from flask import render_template

from yacut import app, db
from yacut.constants import (
    INTERNAL_SERVER_ERROR_MESSAGE,
    PAGE_NOT_FOUND_MESSAGE,
)


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    if hasattr(error, 'response') and error.response:
        return error.response
    return render_template(
        'error.html',
        error=HTTPStatus.NOT_FOUND.value,
        message=PAGE_NOT_FOUND_MESSAGE,
    ), HTTPStatus.NOT_FOUND.value


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    return render_template(
        'error.html',
        error=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        message=INTERNAL_SERVER_ERROR_MESSAGE,
    ), HTTPStatus.INTERNAL_SERVER_ERROR.value