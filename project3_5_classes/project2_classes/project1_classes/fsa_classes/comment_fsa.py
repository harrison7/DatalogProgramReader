from .fsa import FSA
from typing import Callable as function

class CommentFSA(FSA):
    def __init__(self, name):
        FSA.__init__(self, name)
        self.accept_states.add(self.s1)
    
    def s0(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = None
        if current_input == "#": 
            next_state = self.s1
            self.chars_to_delete += 1
        else: next_state = self.s_err
        return next_state

    def s1(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = self.s1
        self.chars_to_delete += 1
        return next_state

    def s_err(self) -> function:
        current_input: str = FSA._FSA__get_current_input(self)
        next_state: function = self.s_err # loop in state s_err
        return next_state