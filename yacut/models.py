import random
import re
from datetime import datetime

from flask import abort, url_for

from yacut import db
from yacut.constants import (
    DUPLICATE_SHORT_WARNING,
    FILES_SHORT,
    INVALID_SHORT_MESSAGE,
    ORIGINAL_MAX_LENGTH,
    REDIRECT_VIEW,
    SHORT_ALLOWED_CHARS,
    SHORT_GENERATION_ATTEMPTS,
    SHORT_LENGTH,
    SHORT_MAX_LENGTH,
    SHORT_PATTERN,
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def create(original, short=None):
        if short:
            URLMap.validate_short(short)
        url_map = URLMap(
            original=original,
            short=short or URLMap.get_unique_short(),
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        url_map = URLMap.get(short)
        if url_map is None:
            abort(404)
        return url_map

    @staticmethod
    def short_exists(short):
        if not short:
            return False
        return short == FILES_SHORT or URLMap.get(short) is not None

    @staticmethod
    def validate_short(short):
        if len(short) > SHORT_MAX_LENGTH or not re.fullmatch(
            SHORT_PATTERN, short
        ):
            raise ValueError(INVALID_SHORT_MESSAGE)
        if URLMap.short_exists(short):
            raise ValueError(DUPLICATE_SHORT_WARNING)

    @staticmethod
    def get_unique_short():
        for _ in range(SHORT_GENERATION_ATTEMPTS):
            short = ''.join(
                random.choices(SHORT_ALLOWED_CHARS, k=SHORT_LENGTH)
            )
            if not URLMap.get(short):
                return short
        raise ValueError(DUPLICATE_SHORT_WARNING)

    def get_short_link(self):
        return url_for(REDIRECT_VIEW, short=self.short, _external=True)
