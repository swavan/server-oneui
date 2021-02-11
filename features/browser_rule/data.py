import uuid
from dataclasses import dataclass, field
from typing import List


@dataclass
class DataHeader:
    key: str = ''
    value: str = ''


@dataclass
class MockData:
    key: uuid = str(uuid.uuid4())
    id: uuid = str(uuid.uuid4())
    content: str = "{" \
                   "}"
    link: str = ""
    status: str = "200"
    content_type: str = "application/json"
    cloud_store_permission: str = "a"
    headers: List[DataHeader] = field(default_factory=list)


@dataclass
class RequestFilter:
    filter_by: str = "q"
    key: str = ""
    value: str = ""


@dataclass
class BrowserRuleResponse:
    id: uuid = str(uuid.uuid4())
    delay: int = 0
    data_source_type: str = "d"
    data: MockData = MockData()
    http_method: str = "al"
    is_logic_enabled: bool = True
    tags: str = "Response"
    filters: List[RequestFilter] = field(default_factory=list)


@dataclass
class Rule:
    id: uuid = str(uuid.uuid4())
    name: str = ""
    description: str = ""
    source_type: str = "u"
    operator: str = "c"
    source: str = ""
    is_enabled: bool = True
    is_favorite: bool = False
    responses: List[BrowserRuleResponse] = field(default_factory=list)
