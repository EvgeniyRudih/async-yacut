from flask import flash, redirect, render_template

from yacut import app
from yacut.constants import REDIRECT_VIEW
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import ShortGenerationError, URLMap
from yacut.yadisk import upload_files_to_disk


@app.route('/', methods=('GET', 'POST'))
def index():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    try:
        url_map = URLMap.create(
            original=form.original_link.data,
            short=form.custom_id.data,
            validate_original=False,
        )
    except ValueError as error:
        flash(str(error))
        return render_template('index.html', form=form)

    return render_template(
        'index.html',
        form=form,
        short_link=url_map.get_short_link(),
    )


@app.route('/files', methods=('GET', 'POST'))
def files():
    form = FileUploadForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)

    try:
        file_names = [file.filename for file in form.files.data]
        download_urls = upload_files_to_disk(
            form.files.data,
            app.config['DISK_TOKEN'],
            app.config['YADISK_API_URL'],
        )
        results = [
            {
                'name': file_name,
                'short_link': URLMap.create(
                    download_url,
                    commit=False,
                ).get_short_link(),
            }
            for file_name, download_url in zip(file_names, download_urls)
        ]
        from yacut import db
        db.session.commit()
    except (ValueError, ShortGenerationError) as error:
        from yacut import db
        db.session.rollback()
        flash(str(error))
        return render_template('files.html', form=form)

    return render_template(
        'files.html',
        form=form,
        results=results,
    )


@app.route('/<string:short>', endpoint=REDIRECT_VIEW)
def redirect_view(short):
    return redirect(URLMap.get_or_404(short).original)
