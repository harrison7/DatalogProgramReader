from typing import Callable
from .project1_classes.token import Token
from .datalog_program import DatalogProgram
from .predicate import Predicate
from .parameter import Parameter
from .rule import Rule

class Parser:  # RDP stands for recursive descent parser
    def __init__(self) -> None:
        ###################################
        # Tuple defining an LL(1) grammar #
        # • set of nonterminals           #
        # • set of terminals              #
        # • starting nonterminal          #
        # • set of productions            #
        ###################################
        self.nonterminals: set[str] = {'datalogProgram', 'schemeList', 'factList', 'ruleList', 
            'queryList', 'scheme', 'fact', 'rule', 'query', 'headPredicate', 'predicate', 
            'predicateList', 'parameterList', 'stringList', 'idList', 'parameter'}  # set of nonterminals. Each nonterminal will have its own function
        self.starting_nonterminal: Callable[[], None] = self.parse_datalog_program     # Starting nonterminal
        self.terminals: set[str] = {'COMMA', 'PERIOD', 'Q_MARK', 'LEFT_PAREN', 'RIGHT_PAREN', 
            'COLON', 'COLON_DASH', 'MULTIPLY', 'ADD', 'SCHEMES', 'FACTS', 'RULES', 'QUERIES', 'ID', 
            'STRING'}  # set of terminals
        # Productions                                   # Defined within the nonterminal functions

        ##########################################
        # Define FIRST sets for each nonterminal #
        ##########################################
        self.first: dict[str, set[str]] = dict()
        self.first['rule'] = {'ID'}
        self.first['query'] = {'ID'}
        self.first['schemeList'] = {'ID'}
        self.first['factList'] = {'ID'}
        self.first['ruleList'] = {'ID'}
        self.first['queryList'] = {'ID'}

        ##########################################
        # Define FOLLOW sets for nonterminal I   #
        ##########################################
        self.follow: dict[str, set[str]] = dict()
        self.follow['schemeList'] = {'FACTS'}
        self.follow['factList'] = {'RULES'}
        self.follow['ruleList'] = {'QUERIES'}
        self.follow['queryList'] = {'EOF'}
        self.follow['predicateList'] = {'PERIOD'}
        self.follow['parameterList'] = {'RIGHT_PAREN'}
        self.follow['stringList'] = {'RIGHT_PAREN'}
        self.follow['idList'] = {'RIGHT_PAREN'}

        ###########################################
        # Variables for Managing the input string #
        ###########################################
        self.datalog_program: DatalogProgram        


    def run(self, tokens: list[Token]) -> str:
        self.index: int = 0
        self.schemes: list[Predicate] = []
        self.facts: list[Predicate] = []
        self.rules: list[Rules] = []
        self.queries: list[Predicate] = []

        self.tokens: list[Token] = tokens
        try:
            self.datalog_program: DatalogProgram = self.starting_nonterminal()
            return "Success!\n" + self.datalog_program.to_string()
        except ValueError as ve:
            return f"Failure!\n  {ve}"

    ##############################################################
    # Each nonterminal gets its own function.                      #
    # The function knows which productions have the nonterminal on #
    # the left hand side of the production. The correct right    #
    # hand side of the production is chosen by looking at the    #
    # current input and the FIRST set of the right hand side     #
    ##############################################################
    def parse_datalog_program(self) -> DatalogProgram:
        self.__match(self.__get_current_input(), 'SCHEMES')
        self.__match(self.__get_current_input(), 'COLON')
        self.schemes.append(self.parse_scheme())
        self.parse_scheme_list()
        # print(self.schemes[0].to_string())

        self.__match(self.__get_current_input(), 'FACTS')
        self.__match(self.__get_current_input(), 'COLON')
        self.parse_fact_list()

        self.__match(self.__get_current_input(), 'RULES')
        self.__match(self.__get_current_input(), 'COLON')
        self.parse_rule_list()

        self.__match(self.__get_current_input(), 'QUERIES')
        self.__match(self.__get_current_input(), 'COLON')
        self.queries.append(self.parse_query())
        self.parse_query_list()
        self.__match(self.__get_current_input(), 'EOF')

        return DatalogProgram(self.schemes, self.facts, self.rules, self.queries)

    def parse_scheme_list(self) -> None:
        if self.__get_current_input() in self.follow['schemeList']:
            return
        else:
            self.schemes.append(self.parse_scheme())
            self.parse_scheme_list()

    def parse_fact_list(self) -> None:
        if self.__get_current_input() in self.follow['factList']:
            return
        else:
            self.facts.append(self.parse_fact())
            self.parse_fact_list()

    def parse_rule_list(self) -> None:
        if self.__get_current_input() in self.follow['ruleList']:
            return
        else:
            self.rules.append(self.parse_rule())
            self.parse_rule_list()

    def parse_query_list(self) -> None:
        if self.__get_current_input() in self.follow['queryList']:
            return
        else:
            self.queries.append(self.parse_query())
            self.parse_query_list()

    def parse_scheme(self) -> Predicate:
        name: str = ''
        parameters: list[Parameter] = []

        self.__match(self.__get_current_input(), 'ID')
        name = self.__get_previous_token()

        self.__match(self.__get_current_input(), 'LEFT_PAREN')
        self.__match(self.__get_current_input(), 'ID')
        parameters.append(Parameter(self.__get_previous_token(), True))
        parameters += self.parse_id_list()
        self.__match(self.__get_current_input(), 'RIGHT_PAREN')

        return Predicate(parameters, name)

    def parse_fact(self) -> Predicate:
        name: str = ''
        parameters: list[Parameter] = []

        self.__match(self.__get_current_input(), 'ID')
        name = self.__get_previous_token()

        self.__match(self.__get_current_input(), 'LEFT_PAREN')
        self.__match(self.__get_current_input(), 'STRING')
        parameters.append(Parameter(self.__get_previous_token(), True))
        parameters += self.parse_string_list()
        self.__match(self.__get_current_input(), 'RIGHT_PAREN')
        self.__match(self.__get_current_input(), 'PERIOD')

        return Predicate(parameters, name)

    def parse_rule(self) -> Rule:
        head_predicate: Predicate = self.parse_head_predicate()
        self.__match(self.__get_current_input(), 'COLON_DASH')

        body_predicates: list[Predicate] = []
        body_predicates.append(self.parse_predicate())
        body_predicates += self.parse_predicate_list()
        self.__match(self.__get_current_input(), 'PERIOD')

        return Rule(head_predicate, body_predicates)

    def parse_query(self) -> Predicate:
        query: Predicate = self.parse_predicate()
        self.__match(self.__get_current_input(), 'Q_MARK')
        return query

    def parse_head_predicate(self) -> Predicate:
        name: str = ''
        parameters: list[Parameter] = []

        self.__match(self.__get_current_input(), 'ID')
        name = self.__get_previous_token()

        self.__match(self.__get_current_input(), 'LEFT_PAREN')
        self.__match(self.__get_current_input(), 'ID')
        parameters.append(Parameter(self.__get_previous_token(), True))
        parameters += self.parse_id_list()
        self.__match(self.__get_current_input(), 'RIGHT_PAREN')

        return Predicate(parameters, name)

    def parse_predicate(self) -> Predicate:
        name: str = ''
        parameters: list[Parameter] = []

        self.__match(self.__get_current_input(), 'ID')
        name = self.__get_previous_token()

        self.__match(self.__get_current_input(), 'LEFT_PAREN')
        parameters.append(self.parse_parameter())
        parameters += self.parse_parameter_list()
        self.__match(self.__get_current_input(), 'RIGHT_PAREN')

        return Predicate(parameters, name)

    def parse_predicate_list(self) -> list[Predicate]:
        if self.__get_current_input() in self.follow['predicateList']:
            return []
        else:
            self.__match(self.__get_current_input(), 'COMMA')
            current_predicate: list[Predicate] = [self.parse_predicate()]

            rest_of_predicates: list[Predicate] = self.parse_predicate_list()
            return current_predicate + rest_of_predicates

    def parse_parameter_list(self) -> list[Parameter]:
        if self.__get_current_input() in self.follow['parameterList']:
            return []
        else:
            self.__match(self.__get_current_input(), 'COMMA')
            current_parameter: list[Parameter] = [self.parse_parameter()]
            
            rest_of_parameters: list[Parameter] = self.parse_parameter_list()
            return current_parameter + rest_of_parameters

    def parse_string_list(self) -> list[Parameter]:
        if self.__get_current_input() in self.follow['stringList']:
            return []
        else:
            self.__match(self.__get_current_input(), 'COMMA')
            self.__match(self.__get_current_input(), 'STRING')
            current_string: list[Parameter] = [Parameter(self.__get_previous_token(), False)]

            rest_of_strings: list[Parameter] = self.parse_string_list()
            return current_string + rest_of_strings

    def parse_id_list(self) -> list[Parameter]:
        if self.__get_current_input() in self.follow['idList']:
            return []
        else:
            self.__match(self.__get_current_input(), 'COMMA')
            self.__match(self.__get_current_input(), 'ID')
            current_id: list[Parameter] = [Parameter(self.__get_previous_token(), True)]

            rest_of_ids: list[Parameter] = self.parse_id_list()
            return current_id + rest_of_ids
            
    def parse_parameter(self) -> Parameter:
        if self.__get_current_input() == 'STRING':
            self.__match(self.__get_current_input(), 'STRING')
            return Parameter(self.__get_previous_token(), False)
        else:
            self.__match(self.__get_current_input(), 'ID')
            return Parameter(self.__get_previous_token(), True)

    ############################################################################
    # Helper functions for managing the input                                    #
    # One looks at the current input                                           #
    # Another reads the input and advances to the next input                  #
    # A third looks to see if the current input character matches a target     #
    # Convention in python is to prefix private functions by a double underscore #
    # https://www.geeksforgeeks.org/private-functions-in-python/                 #
    ############################################################################
    
    def __get_current_input(self) -> str:
        if self.index > len(self.tokens):
            raise ValueError("Expected to read another input character but no inputs left to read")
        else:
            if (self.tokens[self.index].token_type == 'COMMENT'):
                self.__advance_input()
                return self.__get_current_input()
            else:
                return self.tokens[self.index].token_type

    def __advance_input(self) -> None:
        if self.index > len(self.tokens):
            raise ValueError("Expected to advance to the next input character but reached the end of input")
        self.index += 1

    def __match(self, current_input: str, target_input: str) -> None:
        if current_input == target_input:
            self.__advance_input()
        else:
            raise ValueError(self.tokens[self.index].to_string())

    def __get_previous_token(self) -> str:
        return self.tokens[self.index - 1].value

    ########################
    # Other public functions #
    ########################
    def reset(self) -> None:
        self.index = 0
        self.input = []