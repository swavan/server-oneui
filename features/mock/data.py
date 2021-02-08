from dataclasses import dataclass, field
from typing import List


@dataclass
class Header:
    key: str = ""
    value: str = ""

    @classmethod
    def from_model(cls, model): return cls(key=model.get("key", ""), value=model.get("value", ""))


@dataclass
class Rule:
    filter_by: str = ""
    field: str = ""
    operator: str = ""
    value: str = ""

    @classmethod
    def from_model(cls, model):
        return cls(
            filter_by=model.get("filter_by", ""),
            field=model.get("field", ""),
            operator=model.get("operator", ""),
            value=model.get("value", ""))


@dataclass
class Endpoint:
    id: int = 0
    http_method: str = ""
    url: str = ""
    delay: int = ""
    status: str = ""
    content: str = ""
    content_path: str = ""
    headers: List[Header] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            http_method=model.http_method,
            url=model.url,
            delay=model.delay,
            status=model.status,
            content=model.content,
            content_path=model.content_path,
            headers=[Header.from_model(header) for header in model.headers],
            rules=[Rule.from_model(rule) for rule in model.rules])


@dataclass
class EndpointIdentifier:
    id: int = 0
    name: str = ""
    description: str = ""
    selected: bool = False
    endpoints: List[Endpoint] = field(default_factory=list)

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            endpoints=[Endpoint.from_model(endpoint) for endpoint in model.endpoints])


@dataclass
class Mock:
    id: int = 0
    name: str = ""
    port: int = 4001
    delay: int = 0
    status: bool = False
    enable_https: bool = False
    endpointIdentifiers: List[EndpointIdentifier] = field(default_factory=list)

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            port=model.port,
            delay=model.delay,
            endpointIdentifiers=[
                EndpointIdentifier.from_model(endpointIdentifier)
                for endpointIdentifier in model.endpointIdentifiers])
