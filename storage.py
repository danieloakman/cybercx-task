from itertools import islice
from validation import StorageEntry


_storage: dict[str, StorageEntry] = {}


def exists(entry: StorageEntry) -> bool:
    return hash(entry) in _storage


def submit(entry: StorageEntry):
    if exists(entry):
        raise ValueError("Entry already exists")

    _storage[hash(entry)] = entry
    print(_storage)


def get_all() -> list[StorageEntry]:
    return list(_storage.values())


def search(query: str, limit: int, tags: list[str] = []):
    it = filter(lambda entry: query.lower() == entry.value.lower(), _storage.values())
    if tags:
        it = filter(lambda entry: all(tag.lower() in entry.tags for tag in tags), it)
    return list(islice(it, limit))
