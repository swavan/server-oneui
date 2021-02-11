import pickle
from typing import List

from features.browser_rule import data


class BrowserRuleController:

    @classmethod
    def save(cls, _rule: data.Rule, skip: bool = False):
        _rules: List[data.Rule] = cls.load()
        rules = [rule for rule in _rules if rule.id != _rule.id]
        if not skip:
            rules.append(_rule)
        try:
            with open("storage/rules", "wb") as fl:
                pickle.dump(rules, fl)
        finally:
            pass

    @classmethod
    def load(cls) -> List[data.Rule]:
        _rules: List[data.Rule] = []
        try:
            with open("storage/rules", "rb") as fl:
                _rules = pickle.load(fl)
        finally:
            return _rules


