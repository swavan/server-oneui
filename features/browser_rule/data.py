import uuid
from dataclasses import dataclass, field
from typing import Set


@dataclass
class DataHeader:
    key: str = '',
    value: str = ''


@dataclass
class Data:
    key: uuid.uuid4()
    id: uuid = uuid.uuid4()
    content: str = ""
    link: str = ""
    status: str = "200"
    content_type: str = "application/json"
    headers: Set[DataHeader] = field(default_factory=set)
    action_perform: str = 'a'
    is_mock_loading: bool = False


@dataclass
class RequestFilter:
    id: uuid = uuid.uuid4()
    filter_by: str = "n",
    key: str = ""
    value: str = ""
    is_active: bool = True


@dataclass
class BrowserRuleResponse:
    id: uuid = uuid.uuid4()
    delay: int = 0
    mark_for_deletion: bool = False
    data_source_type: str = "r"
    http_method: str = "al"
    is_logic_enabled: bool = True
    cloud_store_permission: str = "a"
    tags: str = ""
    filters: Set[RequestFilter] = field(default_factory=set)


@dataclass
class Rule:
    id: uuid = uuid.uuid4()
    name: str = ""
    description: str = ""
    source_type: str = "u"
    operator: str = "c"
    source: str = ""
    is_enabled: bool = True
    is_favorite: bool = False
    responses: Set[BrowserRuleResponse] = field(default_factory=set)
