from .fsa_classes.fsa import FSA

from .fsa_classes.comma_fsa import CommaFSA
from .fsa_classes.period_fsa import PeriodFSA
from .fsa_classes.q_mark_fsa import QMarkFSA
from .fsa_classes.left_paren_fsa import LeftParenFSA
from .fsa_classes.right_paren_fsa import RightParenFSA
from .fsa_classes.colon_fsa import ColonFSA
from .fsa_classes.colon_dash_fsa import ColonDashFSA
from .fsa_classes.multiply_fsa import MultiplyFSA
from .fsa_classes.add_fsa import AddFSA

from .fsa_classes.schemes_fsa import SchemesFSA
from .fsa_classes.facts_fsa import FactsFSA
from .fsa_classes.rules_fsa import RulesFSA
from .fsa_classes.queries_fsa import QueriesFSA

from .fsa_classes.id_fsa import IDFSA
from .fsa_classes.string_fsa import StringFSA
from .fsa_classes.comment_fsa import CommentFSA

from .token import Token

class Lexer:
    def __init__(self):
        self.tokens: list[Token] = []
        self.line_number: int = 1

        # all FSA's
        self.comma_fsa: CommaFSA = CommaFSA(self)
        self.period_fsa: PeriodFSA = PeriodFSA(self)
        self.q_mark_fsa: QMarkFSA = QMarkFSA(self)
        self.left_paren_fsa: LeftParenFSA = LeftParenFSA(self)
        self.right_paren_fsa: RightParenFSA = RightParenFSA(self)
        self.colon_fsa: ColonFSA = ColonFSA(self)
        self.colon_dash_fsa: ColonDashFSA = ColonDashFSA(self)
        self.multiply_fsa: MultiplyFSA = MultiplyFSA(self)
        self.add_fsa: AddFSA = AddFSA(self)

        self.schemes_fsa: SchemesFSA = SchemesFSA(self)
        self.facts_fsa: FactsFSA = FactsFSA(self)
        self.rules_fsa: RulesFSA = RulesFSA(self)
        self.queries_fsa: QueriesFSA = QueriesFSA(self)

        self.id_fsa: IDFSA = IDFSA(self)
        self.string_fsa: StringFSA = StringFSA(self)
        self.comment_fsa: CommentFSA = CommentFSA(self)

        # list of all FSA outputs
        self.fsa_keys: list[function] = [self.comma_fsa, self.period_fsa, self.q_mark_fsa,
            self.left_paren_fsa, self.right_paren_fsa, self.colon_fsa, self.colon_dash_fsa, 
            self.multiply_fsa, self.add_fsa, self.schemes_fsa, self.facts_fsa, self.rules_fsa,
            self.queries_fsa, self.id_fsa, self.string_fsa, self.comment_fsa]
        
        self.fsa_dict: dict[function, bool] = dict.fromkeys(self.fsa_keys, False)  # Initialize the outputs from each FSA to false
        self.delete_chars: int = 0 # keep track of how many characters to skip after token creation
        self.input_lines: list[str]
        self.current_line: str

    # initialize variables and set up loops for lex()
    def run(self, input: str) -> str:
        if input == "": # if input file is empty
            self.tokens.append(Token("EOF", "", 1))
        else:
            ends_in_newline: bool = (input[-1] == "\n")
            self.input_lines = input.splitlines()

            # Skip empty lines at the end of the file
            while self.input_lines and not self.input_lines[-1].strip():
                self.input_lines.pop()
            for self.current_line in self.input_lines:
                self.current_line = self.current_line.strip()
                while self.current_line != "": # run through each line until entire line converted into tokens
                    while self.current_line and self.current_line[0].isspace():
                        self.current_line = self.current_line[1:] # remove whitespace
                    self.tokens.append(self.lex(self.current_line))

                    if self.tokens[-1].token_type == "UNDEFINED":
                        return self.__create_return_value__(True)

                    self.current_line = self.current_line[self.delete_chars:]
                    self.reset()

                if self.line_number == len(self.input_lines): # end of input, configure EOF token
                    if ends_in_newline: self.line_number += 1
                    self.tokens.append(Token("EOF", "", self.line_number))

                if ends_in_newline:
                    self.line_number += 1

        return self.__create_return_value__(False)
    
    def lex(self, input_string: str) -> Token:
        # Run each FSA on the input and collect their outputs
        for FSA in self.fsa_dict.keys():
            self.fsa_dict[FSA] = FSA.run(input_string)
        # Run the FSM that decides what to do with the outputs of the FSAs
        return self.__manager_fsm__()

    def __manager_fsm__(self) -> Token:
        # A finite state machine implemented as a sequence of if statements
        # Turn the dictionary values into a list
        # print(self.current_line)
        output_list: list[bool] = [value for value in self.fsa_dict.values()]
        if output_list[0] == True:
            output_token: Token = Token("COMMA", ",", self.line_number)
            self.delete_chars = self.comma_fsa.chars_to_delete
        elif output_list[1] == True:
            output_token: Token = Token("PERIOD", ".", self.line_number)
            self.delete_chars = self.period_fsa.chars_to_delete
        elif output_list[2] == True:
            output_token: Token = Token("Q_MARK", "?", self.line_number)
            self.delete_chars = self.q_mark_fsa.chars_to_delete
        elif output_list[3] == True:
            output_token: Token = Token("LEFT_PAREN", "(", self.line_number)
            self.delete_chars = self.left_paren_fsa.chars_to_delete
        elif output_list[4] == True:
            output_token: Token = Token("RIGHT_PAREN", ")", self.line_number)
            self.delete_chars = self.right_paren_fsa.chars_to_delete
        elif output_list[5] == True and output_list[6] == False:
            output_token: Token = Token("COLON", ":", self.line_number)
            self.delete_chars = self.colon_fsa.chars_to_delete
        elif output_list[5] == True and output_list[6] == True:
            output_token: Token = Token("COLON_DASH", ":-", self.line_number)
            self.delete_chars = self.colon_dash_fsa.chars_to_delete
        elif output_list[7] == True:
            output_token: Token = Token("MULTIPLY", "*", self.line_number)
            self.delete_chars = self.multiply_fsa.chars_to_delete
        elif output_list[8] == True:
            output_token: Token = Token("ADD", "+", self.line_number)
            self.delete_chars = self.add_fsa.chars_to_delete
        elif output_list[9] == True:
            output_token: Token = Token("SCHEMES", "Schemes", self.line_number)
            self.delete_chars = self.schemes_fsa.chars_to_delete
        elif output_list[10] == True:
            output_token: Token = Token("FACTS", "Facts", self.line_number)
            self.delete_chars = self.facts_fsa.chars_to_delete
        elif output_list[11] == True:
            output_token: Token = Token("RULES", "Rules", self.line_number)
            self.delete_chars = self.rules_fsa.chars_to_delete
        elif output_list[12] == True:
            output_token: Token = Token("QUERIES", "Queries", self.line_number)
            self.delete_chars = self.queries_fsa.chars_to_delete
        elif output_list[13] == True: # Schemes, Facts, Rules, and Queries are already false at this point
            output_token: Token = Token("ID", self.current_line[0:self.id_fsa.chars_to_delete], self.line_number)
            self.delete_chars = self.id_fsa.chars_to_delete
        elif output_list[14] == True:
            output_token: Token = Token("STRING", self.current_line[0:self.string_fsa.chars_to_delete], self.line_number)
            self.delete_chars = self.string_fsa.chars_to_delete
        elif output_list[15] == True:
            output_token: Token = Token("COMMENT", self.current_line[0:self.comment_fsa.chars_to_delete], self.line_number)
            self.delete_chars = self.comment_fsa.chars_to_delete
        else:
            print(self.current_line)
            output_token: Token = Token("UNDEFINED", str(self.current_line[0]), self.line_number)

        return output_token

    def reset(self) -> None:
        for FSA in self.fsa_dict.keys(): 
            FSA.reset()

    def get_tokens(self) -> list[Token]:
        return self.tokens

    def __create_return_value__(self, error_value: bool) -> str:
        return_value: str = ""
        for token in self.tokens:
            return_value = return_value + token.to_string() + "\n"
        if error_value == False:
            return_value += "Total Tokens = " + str(len(self.tokens)) + "\n"
        else:
            return_value += "\n" + "Total Tokens = Error on line " + str(self.line_number) + "\n"
        return return_value
