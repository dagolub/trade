import datetime
from sqlalchemy.types import DateTime, TypeDecorator  # type: ignore


class UtcDateTime(TypeDecorator):
    """Almost equivalent to :class:`~sqlalchemy.types.DateTime` with
    ``timezone=True`` option, but it differs from that by:

    - Never silently take naive :class:`~datetime.datetime`, instead it
      always raise :exc:`ValueError` unless time zone aware value.
    - :class:`~datetime.datetime` value's :attr:`~datetime.datetime.tzinfo`
      is always converted to UTC.
    - Unlike SQLAlchemy's built-in :class:`~sqlalchemy.types.DateTime`,
      it never return naive :class:`~datetime.datetime`, but time zone
      aware value, even with SQLite or MySQL.

    """

    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, str):
                value = datetime.datetime.fromisoformat(value)
            if not isinstance(value, datetime.datetime):
                raise TypeError("expected datetime.datetime, not " + repr(value))
            elif value.tzinfo is None:
                raise ValueError("naive datetime is disallowed")
            return value.astimezone(datetime.timezone.utc)

    def process_result_value(self, value, dialect):
        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value
