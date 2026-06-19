import string


ORIGINAL_MAX_LENGTH = 256
SHORT_MAX_LENGTH = 16
SHORT_LENGTH = 6
SHORT_GENERATION_ATTEMPTS = 100
SHORT_PATTERN = r'^[a-zA-Z0-9]*$'
SHORT_ALLOWED_CHARS = string.ascii_letters + string.digits

FILES_SHORT = 'files'
REDIRECT_VIEW = 'redirect_view'

INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
EMPTY_REQUEST_BODY_MESSAGE = 'Отсутствует тело запроса'
REQUIRED_FIELD_MESSAGE = '"url" является обязательным полем!'
SHORT_NOT_FOUND_MESSAGE = 'Указанный id не найден'

ORIGINAL_LINK_LABEL = 'Длинная ссылка'
CUSTOM_SHORT_LABEL = 'Ваш вариант короткой ссылки'
CREATE_SUBMIT_LABEL = 'Создать'
FILES_LABEL = 'Файлы'
UPLOAD_SUBMIT_LABEL = 'Загрузить'

PAGE_NOT_FOUND_MESSAGE = 'Страница не найдена'
INTERNAL_SERVER_ERROR_MESSAGE = 'Внутренняя ошибка сервера'
DUPLICATE_SHORT_WARNING = (
    'Предложенный вариант короткой ссылки уже существует.'
)

YADISK_UPLOAD_URL = '/v1/disk/resources/upload'
YADISK_DOWNLOAD_URL = '/v1/disk/resources/download'
YADISK_UPLOAD_PATH = '/yacut/{}'
YADISK_AUTH_HEADER = 'OAuth {}'
