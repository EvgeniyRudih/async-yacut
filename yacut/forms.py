from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from yacut.constants import (
    CREATE_SUBMIT_LABEL,
    CUSTOM_SHORT_LABEL,
    FILES_LABEL,
    ORIGINAL_LINK_LABEL,
    ORIGINAL_MAX_LENGTH,
    SHORT_MAX_LENGTH,
    SHORT_PATTERN,
    UPLOAD_SUBMIT_LABEL,
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(),
            URL(),
            Length(max=ORIGINAL_MAX_LENGTH),
        ],
    )
    custom_id = StringField(
        CUSTOM_SHORT_LABEL,
        validators=[
            Optional(),
            Length(max=SHORT_MAX_LENGTH),
            Regexp(SHORT_PATTERN),
        ],
    )
    submit = SubmitField(CREATE_SUBMIT_LABEL)


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        FILES_LABEL,
        validators=[FileRequired()],
    )
    submit = SubmitField(UPLOAD_SUBMIT_LABEL)
