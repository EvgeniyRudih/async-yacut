import random
import string

from yacut.models import URLMap

CHARACTERS = string.ascii_letters + string.digits
SHORT_ID_LENGTH = 6


def get_unique_short_id():
    while True:
        short_id = ''.join(random.choices(CHARACTERS, k=SHORT_ID_LENGTH))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
