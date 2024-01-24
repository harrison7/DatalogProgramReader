from .fsa import FSA
from typing import Callable as function

class ColonDashFSA(FSA):
    def __init__(self, name):
        FSA.__init__(self, name) # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s2)

    def s0(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input == ':': 
            next_state = self.s1
        else: next_state = self.s_err
        return next_state

    def s1(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input == '-': 
            next_state = self.s2
            self.chars_to_delete = 2
        else: next_state = self.s_err
        return next_state

    def s2(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = self.s2
        return next_state

    def s_err(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state = self.s_err
        return next_state
