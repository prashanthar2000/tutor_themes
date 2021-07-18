# -*- coding: utf-8 -*-
import os
from cms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "host": "mongodb",
    "port": 27017,
    
    "user": None,
    "password": None,
    
    "db": "openedx",
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/"
for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="newrelic.console")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="lms.djangoapps.course_wiki.plugins.markdownedx.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "https://edx3.sapientury.com/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "IOlQzm6dMAwTwkazR5wI500S"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "CAN_Tgy6osIvxJLCjjFMq1-3-kFdK2crIlNfLtg02qvvLb6yonwHSzDcMrym9DXh-X7AHqkTzOtP3AbL7a7XaeoXtLJqy9EY8ygM_TQ-_dBb51Smtt1ZKDO8P3gBarMYGi4y4L1Zo9GXmwSaqTpYJKxrzfXB7H2HjDYSACvcogs2sxygyU8ShgVDtLzoRvSgDjW_6eXjCoZJ7gG_NgpkjcjSrihr47waPsIfiShJr8UPAwbt3e4x3HreqVyzbOVpEH1VGu7WummVOnZ0ikl906RZpfz-1rpRnyHQcVLEHEPalc202fmjbCGQiAXWYCzj6EUy1cFC9xHxN46TRsIF4Q",
        "n": "m844-P3m3tJh1Cv2rIxH6kVbIOpTcANOdOQV8iQUeimFioLzTDDpUrF305kgZRJjZQe2ZseOCuqSNmE3kTcVHkKfk0EqfGHR318oQaxZyrP2FZ7NSv8rxcKacT7QHgmaBAnbwnGsMmOM0TC_S6DjARKoRyqLckMXfYiZsfvCuS3y1TTtZ8ZlhBZZlFXTVvX9OLKSabwQleIiajg8RPfgzRnBf3ZJwa1FtZu1F5BBOAHbAS8rPxFC0x3Az8i1qPd7SQIDu0EwmNplohNqj3q9_GB9Lgq4mWtnmt2W8attWz2oHkiDouVYPrDaNy6ynIjHUXqu8GWgTmtg279h62s48Q",
        "p": "u511TEhrRPBDepvxQ4zG8RXJZaY-to7aHM1eCC77qXYzJ-j7yCKlBQWcL7OLJGwpgICZ6i6sCRDcv94BtVAu5ucac_JkaiTmXihJO4kzgDjQO0dppKSsMF7BJMrjMnUQBLN-KBvT907MeNzeSj584gc9Nxbb3D085iCUBrwO1JE",
        "q": "1JiWkITRAOkNIzxzbU5yUNjMKd8Hz40fT_cXY9RSatOxvUnl7uaIBO2yAVeFcKLpGhuUR5eCH-tLcyPnGGBaRVvQHZgBPaZ1HgrhXHvMNZ9wDZ_RSwm4Rfx_NUZnD-WlBdEsD1SVYECImfHplZtFpEIq5C-FUNnH-4zL227AzmE",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "m844-P3m3tJh1Cv2rIxH6kVbIOpTcANOdOQV8iQUeimFioLzTDDpUrF305kgZRJjZQe2ZseOCuqSNmE3kTcVHkKfk0EqfGHR318oQaxZyrP2FZ7NSv8rxcKacT7QHgmaBAnbwnGsMmOM0TC_S6DjARKoRyqLckMXfYiZsfvCuS3y1TTtZ8ZlhBZZlFXTVvX9OLKSabwQleIiajg8RPfgzRnBf3ZJwa1FtZu1F5BBOAHbAS8rPxFC0x3Az8i1qPd7SQIDu0EwmNplohNqj3q9_GB9Lgq4mWtnmt2W8attWz2oHkiDouVYPrDaNy6ynIjHUXqu8GWgTmtg279h62s48Q",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "https://edx3.sapientury.com/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "IOlQzm6dMAwTwkazR5wI500S"
    }
]

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

# Custom features
# LTI 1.3 will be enabled by default after lilac, and it's going to be a big
# deal, so we enable it early. We should remove this once the feature flag is
# deprecated.
FEATURES["LTI_1P3_ENABLED"] = True


######## End of settings common to LMS and CMS

######## Common CMS settings

STUDIO_NAME = u"My Open edX - Studio"
MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_LOGOUT_URL = LMS_ROOT_URL + '/logout'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE]:
    if not os.path.exists(folder):
        os.makedirs(folder)



######## End of common CMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("CMS_BASE"),
    "cms",
]

