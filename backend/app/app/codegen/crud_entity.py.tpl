from app.crud.base import CRUDBase
from app.models.{{entity_lower}} import {{ entity }}
from app.schemas.{{entity_lower}} import {{ entity }}Create, {{ entity }}Update


class CRUD{{ entity }}(CRUDBase[{{ entity }}, {{ entity }}Create, {{ entity }}Update]):
    pass


{{ entity_lower }} = CRUD{{ entity }}({{ entity }})
