from pony.orm import PrimaryKey, Required, Optional, Set

from storage import db


class Mock(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    port = Required(str)


class EndpointIdentifier(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    endpoints = Set("Endpoint")


class Endpoint(db.Entity):
    id = PrimaryKey(int, auto=True)
    http_method = Required(str)
    url = Required(str)
    delay = Optional(int)
    content_type = Required(str)
    content = Optional(str)
    headers = Set("Header")
    rules = Set("Rule")
    endpointIdentifier = Required(EndpointIdentifier)


class Header(db.Entity):
    id = PrimaryKey(int, auto=True)
    key = Required(str)
    value = Required(str)
    endpoint = Required(Endpoint)


class Rule(db.Entity):
    id = PrimaryKey(int, auto=True)
    filter = Required(str)
    operator = Required(str)
    value = Required(str)
    endpoint = Required(Endpoint)


db.generate_mapping(create_tables=True)
