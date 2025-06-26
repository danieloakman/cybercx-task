from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel
import re


class EntryType(str, Enum):
    IP = "ip"
    DOMAIN = "domain"
    HASH = "hash"  # MD5, SHA1, SHA256


IP_PATTERN = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
DOMAIN_PATTERN = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
HASH_PATTERN = r"^[a-fA-F0-9]{32,64}$"


@dataclass(frozen=True)
class Entry(BaseModel):
    value: str
    tags: list[str] = []

    @property
    def type(self) -> EntryType:
        if re.match(IP_PATTERN, self.value):
            return EntryType.IP
        elif re.match(DOMAIN_PATTERN, self.value):
            return EntryType.DOMAIN
        elif re.match(HASH_PATTERN, self.value):
            return EntryType.HASH
        else:
            raise ValueError("Invalid value format")

    def __hash__(self):
        return hash(self.value + "".join(self.tags) + self.type.value)


class DataRequest(BaseModel):
    q: str
    tags: list[str] = []
    limit: int
