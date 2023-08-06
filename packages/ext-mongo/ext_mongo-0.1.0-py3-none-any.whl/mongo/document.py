from __future__ import annotations

import json
from typing import TypeVar, Any

from .deps import me
from .document_meta import DocumentMeta


class Document(me.Document, metaclass=DocumentMeta):
    meta = {"abstract": True}

    @classmethod
    def get(cls: type[DocT], key: Any) -> DocT | None:
        return cls.find(pk=key)

    @classmethod
    def find(cls: type[DocT], **filters) -> DocT | None:
        return cls.objects(**filters).first()

    @classmethod
    def find_all(cls: type[DocT], **filters) -> list[DocT]:
        return list(cls.objects(**filters))

    @property
    def str_id(self) -> str:
        return str(self.pk)

    def to_dict(self) -> dict:
        return json.loads(self.to_json())


DocT = TypeVar("DocT", bound=Document)
