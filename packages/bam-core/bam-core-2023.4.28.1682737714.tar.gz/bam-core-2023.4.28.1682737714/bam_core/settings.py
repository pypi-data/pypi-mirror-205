import os
import dotenv
import logging
import logging.config

# load .env file
dotenv.load_dotenv()

# DEFAULT SETTINGS

API_VERSION = "v1"
API_KEY_HEADER = "X-BAM-API-KEY"
API_KEY_PARAM = "api_key"

# api spec
APISPEC_SWAGGER_URL = os.getenv("BAM_APISPEC_SWAGGER_URL", "/spec/")
APISPEC_SWAGGER_UI_URL = os.getenv("BAM_APISPEC_SWAGGER_UI_URL", "/docs/")

# bam settings
AIRTABLE_TOKEN = os.getenv("BAM_AIRTABLE_TOKEN", None)
AIRTABLE_BASE_ID = os.getenv("BAM_AIRTABLE_BASE_ID", None)
AIRTABLE_ASSISTANCE_REQUESTS_TABLE_NAME = os.getenv(
    "BAM_AIRTABLE_ASSISTANCE_REQUESTS_TABLE_NAME", "Assistance Requests: Main"
)
AIRTABLE_MESH_VIEW_NAME = os.getenv(
    "BAM_AIRTABLE_MESH_VIEW_NAME", "MESH - Pending installs, by address (Lu)"
)

# flask settings
SECRET_KEY = os.getenv("BAM_SESSION_SECRET_KEY", "secret")

# logging settings
LOG_LEVEL = os.getenv("BAM_LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv(
    "BAM_LOG_FORMAT",
    r"<%(levelname)s> %(module)s:%(lineno)d -> %(message)s [%(asctime)s]",
)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"default": {"format": (LOG_FORMAT)}},
    "datefmt": "%I:%M:%S",
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "default",
        }
    },
    "root": {"level": LOG_LEVEL, "handlers": ["console"]},
}

# listmonk settings

LISTMONK_USERNAME = os.getenv("BAM_LISTMONK_USERNAME", None)
LISTMONK_PASSWORD = os.getenv("BAM_LISTMONK_PASSWORD", None)
LISTMONK_BASE_URL = os.getenv(
    "BAM_LISTMONK_BASE_URL", "https://lists.baml.ink/"
)
if not LISTMONK_BASE_URL.endswith("/"):
    LISTMONK_BASE_URL += "/"

# s3 settings
DO_TOKEN = os.getenv("BAM_DO_TOKEN", None)
S3_BASE_URL = os.getenv(
    "BAM_S3_BASE_URL", "https://nyc3.digitaloceanspaces.com"
)
S3_ENDPOINT_URL = os.getenv(
    "BAM_S3_ENDPOINT_URL", "https://nyc3.digitaloceanspaces.com"
)
S3_ACCESS_KEY_ID = os.getenv("BAM_S3_ACCESS_KEY_ID", None)
S3_SECRET_ACCESS_KEY = os.getenv("BAM_S3_SECRET_ACCESS_KEY", None)
S3_BUCKET = os.getenv("BAM_S3_BUCKET", "bam-file")
S3_REGION_NAME = os.getenv("BAM_S3_REGION_NAME", "nyc3")
S3_PLATFORM = os.getenv("BAM_S3_PLATFORM", "do")
S3_CDN_ID = os.getenv("BAM_S3_CDN_ID", "4d57a938-0336-4bda-a27f-929125be460b")

logging.config.dictConfig(LOGGING_CONFIG)
