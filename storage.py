from itertools import islice
from validation import Entry


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


def search(query: str, limit: int, tags: list[str] = []):
    it = filter(lambda entry: query == entry.value, _storage.values())
    if tags:
        it = filter(lambda entry: all(tag in entry.tags for tag in tags), it)
    return list(islice(it, limit))


# def get_entry(value: str) -> Entry | None:
#     if value in __storage:
#         return __storage[value]
#     return None


# def get_entries_by_tag(tag: str) -> list[Entry]:
#     pass
