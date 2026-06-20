import re
import string


ORIGINAL_MAX_LENGTH = 256
SHORT_MAX_LENGTH = 16
SHORT_LENGTH = 6
SHORT_GENERATION_ATTEMPTS = 100
SHORT_ALLOWED_CHARS = string.ascii_letters + string.digits
SHORT_PATTERN = rf'^[{re.escape(SHORT_ALLOWED_CHARS)}]+$'

FILES_SHORT = 'files'
REDIRECT_VIEW = 'redirect_view'
