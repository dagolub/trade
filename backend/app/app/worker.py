from raven import Client  # type: ignore
from app.core.config import settings

client_sentry = Client(settings.SENTRY_DSN)
