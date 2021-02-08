from datetime import datetime

from typing import Dict

from pony.orm import PrimaryKey, Required, Optional, Set, Json

from storage import db


class Mock(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    port = Required(int, unique=True)
    delay = Required(int)
    is_default = Optional(bool, default=False)
    enable_https = Optional(bool, default=False)
    status = Optional(bool, default=False)
    created = Optional(datetime, default=datetime.now)
    endpointIdentifiers = Set("EndpointIdentifier", cascade_delete=True)

    @classmethod
    def from_dict(cls, raw: Dict):
        row = cls(id=None if raw.get("id", 0) == 0 else raw.get("id", 0),
                  name=raw.get("name"),
                  port=raw.get("port"),
                  delay=raw.get("delay")
                  )
        row.endpointIdentifiers = [EndpointIdentifier.from_dict(endpointIdentifier, row)
                                   for endpointIdentifier in raw.get("endpointIdentifiers", [])]
        return row


class EndpointIdentifier(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    endpoints = Set("Endpoint", cascade_delete=True)
    condition = Optional(bool, default=False)
    order = Optional(bool, default=False)
    created = Optional(datetime, default=datetime.now)
    mock = Required(Mock)

    @classmethod
    def from_dict(cls, raw: Dict, parent: Mock):
        row = cls(id=None if raw.get("id", 0) == 0 else raw.get("id", 0),
                  name=raw.get("name"),
                  description=raw.get("description"),
                  order=raw.get("order",0),
                  mock=parent
                  )
        row.endpoints = [Endpoint.from_dict(endpoint, row) for endpoint in raw.get("endpoints", [])]
        return row


class Endpoint(db.Entity):
    id = PrimaryKey(int, auto=True)
    http_method = Required(str)
    url = Required(str)
    delay = Optional(int)
    status = Required(str)
    content = Optional(str)
    content_path = Optional(str)
    headers = Optional(Json)
    rules = Optional(Json)
    endpoint_identifier = Required(EndpointIdentifier)
    condition = Optional(bool, default=False)
    order = Optional(int, auto=True)
    created = Optional(datetime, default=datetime.now)

    @classmethod
    def from_dict(cls, raw: Dict, parent: EndpointIdentifier):
        return cls(id=None if raw.get("id", 0) == 0 else raw.get("id", 0),
                   http_method=raw.get("http_method", ""),
                   url=raw.get("url", ""),
                   delay=raw.get("delay", ""),
                   status=raw.get("status", ""),
                   content=raw.get("content", ""),
                   content_path=raw.get("content_path", ""),
                   headers=raw.get("headers", []),
                   rules=raw.get("rules", []),
                   order=raw.get("order", 0),
                   condition=raw.get("condition", 1),
                   endpoint_identifier=parent)


db.generate_mapping(create_tables=True)
