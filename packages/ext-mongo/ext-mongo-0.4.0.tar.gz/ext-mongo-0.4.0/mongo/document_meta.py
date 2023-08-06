from datetime import datetime, date

from bson import ObjectId
from mongoengine.base import TopLevelDocumentMetaclass

from mongo import me


class PrimaryKey:
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
    if _type == dict:
        return me.DictField()

    for t, Field in FIELD_BY_TYPE.items():
        if _type == t | PrimaryKey:
            return Field(primary_key=True)
        if _type == t | None:
            return Field()
        if _type == t:
            return Field(required=True)
        if _type == list[t]:
            return me.ListField(Field())

    msg = f"Can't make field `{name}` with type {repr(_type)}"
    raise ValueError(msg)


FIELD_BY_TYPE = {
    str: me.StringField,
    int: me.IntField,
    bool: me.BooleanField,
    float: me.FloatField,
    ObjectId: me.ObjectIdField,
    datetime: me.DateTimeField,
    date: me.DateField,
}
