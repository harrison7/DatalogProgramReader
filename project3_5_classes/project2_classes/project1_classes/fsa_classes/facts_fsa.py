from .fsa import FSA
from typing import Callable as function

class FactsFSA(FSA):
    def __init__(self, name):
        FSA.__init__(self, name)
        self.accept_states.add(self.s5)
        self.accept_states.add(self.s6)

    def s0(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input == 'F': 
            next_state = self.s1
        else: next_state = self.s_err
        return next_state

    def s1(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input == 'a': 
            next_state = self.s2
        else: next_state = self.s_err
        return next_state

    def s2(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input == 'c': 
            next_state = self.s3
        else: next_state = self.s_err
        return next_state

    def s3(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input == 't': 
            next_state = self.s4
        else: next_state = self.s_err
        return next_state

    def s4(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input == 's':
            next_state = self.s5
            self.chars_to_delete = 5
        else: next_state = self.s_err
        return next_state

    def s5(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input.isalnum():
            next_state = self.s_err
        else: next_state = self.s6
        return next_state

    def s6(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = self.s6
        return next_state

    def s_err(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state = self.s_err
        return next_state
