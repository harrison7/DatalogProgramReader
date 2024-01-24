from typing import Dict
from .relation import Relation

class Database:
    def __init__(self) -> None:
        self.database: Dict[str, Relation] = {}

    def add_relation(self, name: str, relation: Relation) -> None:
        self.database[name] = relation

    def get_relation(self, name: str) -> Relation:
        return self.database[name]

    def reset(self) -> None:
        self.database: Dict[str, Relation] = {}