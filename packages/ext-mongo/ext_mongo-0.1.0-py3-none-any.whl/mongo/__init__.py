import env

from .connect import connect
from .deps import me
from .document import Document
from .document_meta import PrimaryKey

connect(
    db=env.get("MONGO_DB"),
    host=env.get("MONGO_HOST", None),
    password=env.get("MONGO_PASSWORD", None),
    user=env.get("MONGO_USER", None),
    port=env.get_int("MONGO_PORT", None),
)

__all__ = ["Document", "me", "PrimaryKey"]
