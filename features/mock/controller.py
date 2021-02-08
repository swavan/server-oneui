from datetime import datetime
from dataclasses import asdict
from typing import List, Tuple

from pony.orm import db_session, select, desc

from features.mock import data, model


@db_session
def save_mock_server(mock: data.Mock) -> Tuple[str, bool]:
    server = model.Mock.get(port=mock.port)
    if server and server.id != mock.id:
        return "Port already in use", False
    server = model.Mock.get(name=mock.name)
    if server and server.id != mock.id :
        return "Mock name already in use", False

    if mock.id > 0:
        server = model.Mock.get_for_update(id=mock.id)
        if server:
            server.name = mock.name
            server.delay = mock.delay
            server.port = mock.port
        return "Mock configuration Updated", True
    else:
        model.Mock.from_dict(asdict(mock))
        return "New mock server created", True


@db_session
def get_last_seen_mock(mock_id: int = 0) -> data.Mock:
    if mock_id > 0:
        mock = model.Mock.get(id=mock_id)
        if mock:
            return data.Mock.from_model(mock)
        return data.Mock()

    query = model.Mock.select(lambda x: x)
    mock = query.sort_by(desc(model.Mock.created)).first()
    return data.Mock.from_model(mock)


@db_session
def load_mock_servers() -> List[data.Mock]:
    query = model.Mock.select(lambda x: x)
    sorted_mocks = query.sort_by(desc(model.Mock.created))
    return [data.Mock.from_model(_mock) for _mock in sorted_mocks]


@db_session
def remove_mock_server(_id: int) -> bool:
    row = model.Mock.get(id=_id)
    if row:
        row.delete()
        return True
    return False


@db_session
def load_endpoint_identifier(_id: int) -> data.EndpointIdentifier:
    _endpoint_identifier = model.EndpointIdentifier \
        .select(lambda _endpoint_identifier: _endpoint_identifier.id == _id) \
        .get()
    if _endpoint_identifier:
        return data.EndpointIdentifier.from_model(_endpoint_identifier)
    return data.EndpointIdentifier()


@db_session
def load_endpoint_identifiers(mock_id: int = 0) -> List[data.EndpointIdentifier]:
    if mock_id == 0:
        return []
    mock = model.Mock.get(id=mock_id)
    query = model.EndpointIdentifier.select(lambda x: x.mock == mock)
    sorted_mocks = query.sort_by(desc(model.EndpointIdentifier.created))
    return [data.EndpointIdentifier.from_model(_mock) for _mock in sorted_mocks]


@db_session
def save(endpoint_identifier: data.EndpointIdentifier, mock_id: int = 0) -> None:

    if endpoint_identifier.id == 0:
        if mock_id == 0:
            return
        mock = model.Mock.get(id=mock_id)
        endpoint_identifier = model.EndpointIdentifier.from_dict(asdict(endpoint_identifier), mock)
        endpoint_identifier.mock = mock
    else:
        _endpoint_identifier = model.EndpointIdentifier.get_for_update(id=endpoint_identifier.id)
        _endpoint_identifier.name = endpoint_identifier.name
        _endpoint_identifier.description = endpoint_identifier.description

        updatable_endpoints = set(map(lambda x: x.id, endpoint_identifier.endpoints))
        for endpoint in _endpoint_identifier.endpoints:
            if endpoint.id not in updatable_endpoints:
                endpoint.delete()

        for endpoint in endpoint_identifier.endpoints:
            if endpoint.id == 0:
                model.Endpoint.from_dict(asdict(endpoint), _endpoint_identifier)
            else:
                _endpoint = model.Endpoint.get_for_update(id=endpoint.id)
                if _endpoint:
                    _endpoint.http_method = endpoint.http_method
                    _endpoint.url = endpoint.url
                    _endpoint.delay = endpoint.delay
                    _endpoint.status = endpoint.status
                    _endpoint.content = endpoint.content
                    _endpoint.content_path = endpoint.content_path
                    _endpoint.headers = [asdict(header) for header in endpoint.headers]
                    _endpoint.rules = [asdict(rule) for rule in endpoint.rules]


@db_session
def remove_endpoint_identifier(_id: int) -> bool:
    row = model.EndpointIdentifier.get(id=_id)
    if row:
        row.delete()
        return True
    return False
