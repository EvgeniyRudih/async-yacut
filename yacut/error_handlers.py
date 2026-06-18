from flask import render_template

from yacut import app


@app.errorhandler(404)
def page_not_found(error):
    if hasattr(error, 'response') and error.response:
        return error.response
    return render_template('error.html', error=404,
                           message='Страница не найдена'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error=500,
                           message='Внутренняя ошибка сервера'), 500
