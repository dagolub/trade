from app.crud.base import CRUDBase
from app.models.folder import Folder
from app.schemas.folder import FolderCreate, FolderUpdate


class CRUDFolder(CRUDBase[Folder, FolderCreate, FolderUpdate]):
    pass


folder = CRUDFolder(Folder)
