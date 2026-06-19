from flask import flash, redirect, render_template, url_for

from yacut import app
from yacut.constants import DUPLICATE_SHORT_WARNING, REDIRECT_VIEW
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.yadisk import upload_files_to_disk


@app.route('/', methods=('GET', 'POST'))
def index():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    if URLMap.short_exists(form.custom_id.data):
        flash(DUPLICATE_SHORT_WARNING)
        return render_template('index.html', form=form)

    url_map = URLMap.create(
        original=form.original_link.data,
        short=form.custom_id.data,
    )
    return render_template(
        'index.html',
        form=form,
        short_link=url_map.get_short_link(),
    )


@app.route('/files', methods=('GET', 'POST'))
def files():
    form = FileUploadForm()
    if not form.validate_on_submit():
        return render_template(
            'files.html',
            files_url=url_for('files'),
            form=form,
            results=[],
        )

    results = [
        {
            'name': file_name,
            'short_link': URLMap.create(download_url).get_short_link(),
        }
        for file_name, download_url in upload_files_to_disk(form.files.data)
    ]
    return render_template(
        'files.html',
        files_url=url_for('files'),
        form=form,
        results=results,
    )


@app.route('/<string:short>', endpoint=REDIRECT_VIEW)
def redirect_view(short):
    return redirect(URLMap.get_or_404(short).original)
