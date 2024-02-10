from app.crud.base import CRUDBase
from app.models.page import Page
from app.schemas.page import PageCreate, PageUpdate


class CRUDPage(CRUDBase[Page, PageCreate, PageUpdate]):
    async def get_by_title(self, db, title):
        if not isinstance(title, (list)):
            title = [title]
        result = []
        async for instance in db[self.model.__tablename__].find(
            {"title": {"$in": title}}
        ):
            instance["id"] = str(instance["_id"])
            result.append(instance)
        return result


page = CRUDPage(Page)
