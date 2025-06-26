from enum import Enum
from pydantic import BaseModel, Field, field_validator
import re


class EntryType(str, Enum):
    IP = "ip"
    DOMAIN = "domain"
    HASH = "hash"  # MD5, SHA1, SHA256


IP_PATTERN = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
DOMAIN_PATTERN = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
HASH_PATTERN = r"^[a-fA-F0-9]{32,64}$"


def validate_value(v: str) -> str:
    if not v.strip():
        raise ValueError("Value cannot be empty or whitespace only")

    if re.match(IP_PATTERN, v):
        return v.lower()
    elif re.match(DOMAIN_PATTERN, v):
        return v.lower()
    elif re.match(HASH_PATTERN, v):
        return v.lower()
    else:
        raise ValueError(
            "Value must be a valid IP address, domain name, or hash (MD5/SHA1/SHA256). "
            "IP format: xxx.xxx.xxx.xxx, Domain format: example.com, "
            "Hash format: 32-64 character hexadecimal string"
        )


def validate_tags(v: list[str]) -> list[str]:
    for tag in v:
        if not tag.strip():
            raise ValueError("Tags cannot be empty or whitespace only")
        if len(tag) > 50:
            raise ValueError(f"Tag '{tag}' is too long (max 50 characters)")
    return [tag.lower() for tag in v]


def get_type(v: str) -> EntryType:
    if re.match(IP_PATTERN, v):
        return EntryType.IP
    elif re.match(DOMAIN_PATTERN, v):
        return EntryType.DOMAIN
    elif re.match(HASH_PATTERN, v):
        return EntryType.HASH
    else:
        raise ValueError("Invalid value format")


ValueField = Field(
    ..., min_length=1, description="The value to store (IP, domain, or hash)"
)

TagsField = Field(default=[], description="Optional tags for categorization")


class StorageEntry(BaseModel):
    value: str = ValueField
    tags: list[str] = TagsField

    @field_validator("value")
    def validate_value_format(cls, v):
        return validate_value(v)

    @field_validator("tags")
    def validate_tags(cls, v):
        return validate_tags(v)

    @property
    def type(self) -> EntryType:
        return get_type(self.value)

    def __hash__(self):
        return hash(self.value + "".join(self.tags) + self.type.value)

    def model_dump(self, **kwargs):
        """Override model_dump to include the type property"""
        data = super().model_dump(**kwargs)
        data["type"] = self.type.value
        return data

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "value": "192.168.1.1",
                "tags": ["internal", "router"],
                "type": "ip",
            }
        }


class DataParams(BaseModel):
    q: str = ValueField
    tags: list[str] = TagsField
    limit: int = Field(
        ..., gt=0, le=1000, description="Maximum number of results to return"
    )

    @field_validator("q")
    def validate_query(cls, v):
        return validate_value(v)

    @field_validator("tags")
    def validate_tags(cls, v):
        return validate_tags(v)

    @property
    def type(self) -> EntryType:
        return get_type(self.q)

    def to_result(self):
        return {
            "value": self.q,
            "tags": self.tags,
            "type": self.type,
        }

    class ConfigDict:
        json_schema_extra = {
            "example": {"q": "192.168.1.1", "tags": ["internal"], "limit": 10}
        }
