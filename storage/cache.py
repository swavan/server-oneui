import pickle
from dataclasses import dataclass, field
from typing import Set


@dataclass
class OneUIMockCache:
    current_server: int = 0
    selected_endpoint_identifier: int = 0
    running_server: Set[int] = field(default_factory=set)


class OneUIApplicationCache:
    mock: OneUIMockCache = OneUIMockCache()


class Store:
    @classmethod
    def save(cls):
        with open(".swavan_state", "wb") as fl:
            pickle.dump(OneUIApplicationCache, fl)

    @classmethod
    def load(cls):
        pass

