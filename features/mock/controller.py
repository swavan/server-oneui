from pony.orm import db_session

from features.mock.model import EndpointIdentifier


@db_session
def save_endpoint_identifier(name, description) -> EndpointIdentifier:
    endpoint = EndpointIdentifier(name=name, description=description)
    return endpoint

