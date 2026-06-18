from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.yadisk import upload_files_to_disk


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id == 'files' or URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        if not custom_id:
            custom_id = get_unique_short_id()
        url_map = URLMap(original=form.original_link.data, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        short_link = url_for('redirect_view', short_id=custom_id, _external=True)
        return render_template('index.html', form=form, short_link=short_link)
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
def files():
    form = FileUploadForm()
    results = []
    if form.validate_on_submit():
        uploaded_files = form.files.data
        results = upload_files_to_disk(uploaded_files)
    return render_template('files.html', form=form, results=results)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
