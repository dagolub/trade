from app.core.config import settings
import sentry_sdk

sentry_sdk.init(
    dsn=settings.SENTRY_DSN, enable_tracing=True, environment=settings.ENVIRONMENT
)
