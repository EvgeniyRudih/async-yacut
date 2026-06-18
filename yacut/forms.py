from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(), URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=16),
            Regexp(r'^[a-zA-Z0-9]*$')
        ]
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[FileRequired()]
    )
    submit = SubmitField('Загрузить')
