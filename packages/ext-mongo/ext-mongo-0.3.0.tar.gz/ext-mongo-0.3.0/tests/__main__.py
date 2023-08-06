from datetime import datetime, date

from bson import ObjectId

from mongo import Document, PrimaryKey


class Doc(Document):
    key: PrimaryKey[int]
    a1: str  # Required
    a2: int | None
    a3: bool | None
    a4: float | None
    a5: ObjectId | None
    a6: datetime | None
    a7: date | None
    b1: list[str]
    b2: list[int]
    b3: list[bool]
    b4: list[float]
    b5: list[ObjectId]
    b6: list[datetime]
    b7: list[date]
    c1: dict
    c2: list[dict]


KEY = 0
A1 = "a1"

d = Doc(key=KEY, a1=A1).save()

assert Doc.get(KEY) == d
assert Doc.find(a1=A1) == d
assert Doc.find_all(a1=A1) == [d]
assert d.str_id == str(KEY)
assert d.to_dict() == {
    "_id": KEY,
    "a1": A1,
    "b1": [],
    "b2": [],
    "b3": [],
    "b4": [],
    "b5": [],
    "b6": [],
    "b7": [],
    "c1": {},
    "c2": [],
}
