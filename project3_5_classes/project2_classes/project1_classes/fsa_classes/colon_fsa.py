from .fsa import FSA
from typing import Callable as function

class ColonFSA(FSA):
    def __init__(self, name):
        FSA.__init__(self, name) # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s1) # Since self.accept_states is defined in parent class, I can use it here
    
    def s0(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input == ':': 
            next_state = self.s1
            self.chars_to_delete = 1
        else: next_state = self.s_err
        return next_state

    def s1(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = self.s1 # loop in state s1
        return next_state

    def s_err(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = self.s_err # loop in state s_err
        return next_state