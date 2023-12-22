from app.crud.base import CRUDBase
from app.models.apikey import Apikey
from app.schemas.apikey import ApikeyCreate, ApikeyUpdate


class CRUDApikey(CRUDBase[Apikey, ApikeyCreate, ApikeyUpdate]):
    async def get_by_apikey(self, db, token):
        apikey = await db["apikey"].find_one({"apikey": token})
        if apikey:  # type: ignore
            apikey["id"] = str(apikey["_id"])
        return apikey


apikey = CRUDApikey(Apikey)
