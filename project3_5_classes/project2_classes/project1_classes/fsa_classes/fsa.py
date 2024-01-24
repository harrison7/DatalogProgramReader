from typing import Callable as function

class FSA:
    def __init__(self, name: str):
        """ Finite state automata must have a 
        • set of states 
        • start state
        • input alphabet
        • set of accept states
        • transition function
        """
        self.fsa_name: str = name                   # name of state machine
        self.start_state: function = self.s0        # start state always named s0 in this implementation
        self.accept_states: set[function] = set()   # set of accept states must be specified in derived class
        self.input_string: str = ""                 # input string
        self.num_chars_read: int = 0                # current input character
        self.chars_to_delete: int = 0
    
    def s0(self) -> None:
        """ Every FSA must have a start state, and we'll always name 
        it s0. The function for the start state must be defined in the
        derived class since it's not defined here. """
        raise NotImplementedError()
    
    def run(self, input_string: str) -> bool:
        """ The workhorse of the FSA shared by all the FSAs in project 1.
        • record the input string
        • initialize the start state
        • while there are still characters to read in the input string ...
        • transition between states
        • return something useful if the final state is an accept state """
        self.input_string = input_string
        current_state: function = self.start_state
        while self.num_chars_read < len(self.input_string):
            current_state = current_state()
        if current_state in self.accept_states:
            return True # Output if the FSA ended in an accept state
        else: 
            return False # Output if the FSA ended in anything other than an accept state

    def reset(self) -> None:
        self.num_chars_read = 0
        self.input_string = ""
        self.chars_to_delete = 0

    def get_name(self) -> str:
        return self.fsa_name

    def set_name(self, FSA_name) -> None:
        self.fsa_name = FSA_name

    def __get_current_input(self) -> str:  # The double underscore makes the method private
        current_input: str = self.input_string[self.num_chars_read]
        self.num_chars_read += 1
        return current_input