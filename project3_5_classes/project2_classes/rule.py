from .predicate import Predicate

class Rule():
    def __init__(self, head_predicate: Predicate, body_predicates: list[Predicate]):
        self.head_predicate = head_predicate
        self.body_predicates = body_predicates

    def to_string(self) -> str:
        predicate_string: str = ''
        predicate_string = ','.join(pred.to_string() for pred in self.body_predicates)
        return(f'{self.head_predicate.to_string()} :- {predicate_string}')