import random
import re
from datetime import datetime

from flask import url_for

from yacut import db
from yacut.constants import (
    ORIGINAL_MAX_LENGTH,
    REDIRECT_VIEW,
    RESERVED_SHORTS,
    SHORT_ALLOWED_CHARS,
    SHORT_GENERATION_ATTEMPTS,
    SHORT_LENGTH,
    SHORT_MAX_LENGTH,
    SHORT_PATTERN,
)


INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
DUPLICATE_SHORT_WARNING = (
    'Предложенный вариант короткой ссылки уже существует.'
)
SHORT_GENERATION_ERROR_MESSAGE = (
    f'Не удалось сгенерировать короткую ссылку. '
    f'Количество попыток: {SHORT_GENERATION_ATTEMPTS}.'
)
ORIGINAL_TOO_LONG_MESSAGE = ORIGINAL_TOO_LONG_MESSAGE = (
    f'Максимальная длина исходной ссылки — '
    f'Количество символов: {ORIGINAL_MAX_LENGTH}.'
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    class ShortGenerationError(Exception):
        pass

    @staticmethod
    def create(
        original,
        short=None,
        validate_original=True,
        validate_short=True,
        commit=True,
    ):
        if validate_original and len(original) > ORIGINAL_MAX_LENGTH:
            raise ValueError(ORIGINAL_TOO_LONG_MESSAGE)

        if short and validate_short:
            if len(short) > SHORT_MAX_LENGTH or not re.fullmatch(
                SHORT_PATTERN, short
            ):
                raise ValueError(INVALID_SHORT_MESSAGE)
            if URLMap.short_exists(short):
                raise ValueError(DUPLICATE_SHORT_WARNING)

        url_map = URLMap(
            original=original,
            short=short or URLMap.get_unique_short(),
        )
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def short_exists(short):
        return short in RESERVED_SHORTS or URLMap.get(short)

    @staticmethod
    def get_unique_short():
        for _ in range(SHORT_GENERATION_ATTEMPTS):
            short = ''.join(
                random.choices(SHORT_ALLOWED_CHARS, k=SHORT_LENGTH)
            )
            if not URLMap.short_exists(short):
                return short
        raise URLMap.ShortGenerationError(SHORT_GENERATION_ERROR_MESSAGE)

    def get_short_link(self):
        return url_for(REDIRECT_VIEW, short=self.short, _external=True)
