

class SandboxConfig(object):
    SECRET_KEY = 'B43EA47481FD02AD6131D24BF494DCCF358A349C403F2F39C0E141D596E9FEBC'  # SHA256 АсенийЛевАлексей
    DEBUG = True
    HOST = 'localhost'
    DATABASE_URL = 'business_diving'
    USERNAME = 'postgres'
    PASSWORD = 'postgres'
    # UPLOAD_FOLDER = '/uploads'
    # ALLOWED_EXTENSIONS = set(['pdf', 'ppt', 'pptx', 'xls', 'xlsx', 'doc', 'docx'])
    # REMEMBER_COOKIE_DURATION = timedelta(days=4)  # days
    # MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 mb
    # TOKEN_LIFETIME = 72  # hours #для нормального времени вернуть 48 часов
    # INVITE_LINK = 'join'
    # RESET_PASSWORD_LINK = 'resetPassword'
    #
    # TEAMS_ON_ONE_SEARCH_PAGE = 10
    # EMAIL_SERVER = 'smtp.yandex.com'
    # EMAIL_LOGIN = 'alex87e.ae@yandex.ru'
    # EMAIL_PASSWORD = 'Warhawk1987'
    # EMAIL_MAIL_FROM = 'alex87e.ae@yandex.ru'
    # EMAIL_MAIN_DOMEN = 'business-diving.ru'


class ProductionConfig(object):
    SECRET_KEY = 'B43EA47481FD02AD6131D24BF494DCCF358A349C403F2F39C0E141D596E9FEBC'  # SHA256 АсенийЛевАлексей
    DEBUG = False
    HOST = 'localhost'
    DATABASE_URL = 'business_diving'
    USERNAME = 'app_user'
    PASSWORD = 'qwerty_123'
    # UPLOAD_FOLDER = '/uploads'
    # ALLOWED_EXTENSIONS = set(['pdf', 'ppt', 'pptx', 'xls', 'xlsx', 'doc', 'docx'])
    # REMEMBER_COOKIE_DURATION = timedelta(days=4)  # days
    # MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 mb
    # TOKEN_LIFETIME = 72  # hours #для нормального времени вернуть 48 часов
    # INVITE_LINK = 'join'
    # RESET_PASSWORD_LINK = 'resetPassword'
    #
    # TEAMS_ON_ONE_SEARCH_PAGE = 10
    # EMAIL_SERVER = 'smtp.yandex.com'
    # EMAIL_LOGIN = 'info@business-diving.ru'
    # EMAIL_PASSWORD = 'A5palich'
    # EMAIL_MAIL_FROM = 'info@business-diving.ru'
    # EMAIL_MAIN_DOMEN = 'business-diving.ru'