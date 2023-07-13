from typing import Optional
from pydantic import BaseModel
from bson.objectid import ObjectId


class {{ entity }}Base(BaseModel):{% if schema_fields %}
    {% for field in schema_fields %}{{ schema_fields[field] }}
    {% endfor %}
    {% else %}
    pass
    {% endif %}
class {{ entity }}Create({{ entity }}Base):
    pass


class {{ entity }}Update({{ entity }}Base):
    pass


class {{ entity }}InDBBase({{ entity }}Base):
    _id: ObjectId
    {% for field in related_fields %}
        {{ field }}_id: int
    {% endfor %}
    class Config:
        orm_mode = True


class {{ entity }}({{ entity }}InDBBase):
    pass


class {{ entity }}InDB({{ entity }}InDBBase):
    pass
