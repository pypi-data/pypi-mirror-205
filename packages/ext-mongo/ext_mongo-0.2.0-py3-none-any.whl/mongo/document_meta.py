from datetime import datetime, date
from typing import TypeVar, Generic

from bson import ObjectId
from mongoengine.base import TopLevelDocumentMetaclass

from mongo import me

T = TypeVar("T")


class PrimaryKey(Generic[T]):
    pass


class DocumentMeta(TopLevelDocumentMetaclass):
    def __new__(mcs, name, parents: tuple[type], attrs: dict):
        return super().__new__(mcs, name, parents, attrs | make_fields(attrs))


def make_fields(attrs: dict) -> dict:
    fields = {}
    anns = attrs.get("__annotations__", {}).items()
    for attr, _type in anns:
        if attr not in attrs:
            fields[attr] = make_field(_type, attr)
    return fields


def make_field(_type: type, name: str):
    kwargs = {}

    if getattr(_type, "__origin__", None) == PrimaryKey:
        _type = getattr(_type, "__args__")[0]
        kwargs = {"primary_key": True}

    for t, Field in FIELD_BY_TYPE.items():
        if _type == t and _type != dict:
            kwargs["required"] = True
        field = Field(**kwargs)
        if _type in [t, t | None]:
            return field
        if _type == list[t]:
            me.DictField()
            return me.ListField(field)

    msg = f"Can't make field `{name}` with type {repr(_type)}"
    raise ValueError(msg)


FIELD_BY_TYPE = {
    str: me.StringField,
    int: me.IntField,
    bool: me.BooleanField,
    float: me.FloatField,
    dict: me.DictField,
    ObjectId: me.ObjectIdField,
    datetime: me.DateTimeField,
    date: me.DateField,
}
