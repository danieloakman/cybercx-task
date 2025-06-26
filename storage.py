from validation import DataRequest, Entry
from itertools import islice


_storage: dict[str, Entry] = {}


def exists(entry: Entry) -> bool:
    return hash(entry) in _storage


def submit(entry: Entry):
    if exists(entry):
        raise ValueError("Entry already exists")

    _storage[hash(entry)] = entry
    print(_storage)

def get_all() -> list[Entry]:
    return list(_storage.values())

def search(req: DataRequest):
    it = filter(lambda entry: req.q == entry.value, _storage.values())
    if req.tags:
        it = filter(lambda entry: all(tag in entry.tags for tag in req.tags), it)
    return list(islice(it, req.limit))


# def get_entry(value: str) -> Entry | None:
#     if value in __storage:
#         return __storage[value]
#     return None


# def get_entries_by_tag(tag: str) -> list[Entry]:
#     pass
