from flask import flash, redirect, render_template

from yacut import app
from yacut.constants import REDIRECT_VIEW
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.yadisk import upload_files_to_disk


@app.route('/', methods=('GET', 'POST'))
def index():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    try:
        return render_template(
            'index.html',
            form=form,
            short_link=URLMap.create(
                original=form.original_link.data,
                short=form.custom_id.data,
                validate_original=False,
            ).get_short_link(),
        )
    except (ValueError, URLMap.ShortGenerationError) as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/files', methods=('GET', 'POST'))
def files():
    form = FileUploadForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)

    try:
        download_urls = upload_files_to_disk(form.files.data)
    except Exception as error:
        flash(str(error))
        return render_template('files.html', form=form)

    try:
        results = []
        files_count = len(form.files.data)
        for index, (file, download_url) in enumerate(
            zip(form.files.data, download_urls),
            start=1,
        ):
            results.append(
                {
                    'name': file.filename,
                    'short_link': URLMap.create(
                        download_url,
                        commit=index == files_count,
                    ).get_short_link(),
                }
            )
    except (ValueError, URLMap.ShortGenerationError) as error:
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
