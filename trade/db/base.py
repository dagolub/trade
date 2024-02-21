# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # type: ignore  # noqa
from app.models.user import User  # type: ignore  # noqa
