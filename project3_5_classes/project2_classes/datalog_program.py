from .predicate import Predicate
from .parameter import Parameter
from .rule import Rule

class DatalogProgram():
    def __init__(self, schemes: list[Predicate], facts: list[Predicate], rules: list[Rule], 
        queries: list[Predicate]):
        self.schemes = schemes
        self.facts = facts
        self.rules = rules
        self.queries = queries

        self.scheme_length: int = len(self.schemes)
        self.fact_length: int = len(self.facts)
        self.rule_length: int = len(self.rules)
        self.query_length: int = len(self.queries)

    def to_string(self):
        scheme_list: str = ''
        fact_list: str = ''
        rule_list: str = ''
        query_list: str = ''
        domain_set: list[str] = []
        domain_list: str = ''

        for i in range(self.scheme_length):
            scheme_list = scheme_list + "  " + self.schemes[i].to_string() + "\n"

        for i in range(self.fact_length):
            fact_list = fact_list + "  " + self.facts[i].to_string() + ".\n"

        for i in range(self.rule_length):
            rule_list = rule_list + "  " + self.rules[i].to_string() + ".\n"

        for i in range(self.query_length):
            query_list = query_list + "  " + self.queries[i].to_string() + "?\n"

        for i in range(self.fact_length):
            for j in range(self.facts[i].length):
                domain_set.append(self.facts[i].parameters[j].to_string())
        # domain_set = sorted(domain_set)
        domain_set = sorted(list(set(domain_set)))
        for i in range(len(domain_set)):
            domain_list = domain_list + "  " + domain_set[i] + "\n"

        return "Schemes(" + str(self.scheme_length) + "):\n" + scheme_list + \
                    "Facts(" + str(self.fact_length) + "):\n" + fact_list + \
                    "Rules(" + str(self.rule_length) + "):\n" + rule_list + \
                    "Queries(" + str(self.query_length) + "):\n" + query_list + \
                    "Domain(" + str(len(domain_set)) + "):\n" + domain_list