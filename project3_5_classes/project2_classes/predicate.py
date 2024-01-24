from .parameter import Parameter

class Predicate():
    def __init__(self, parameters: list[Parameter], name: str):
        self.parameters = parameters
        self.name = name
        
        self.length: int = len(self.parameters)

    def to_string(self) -> str:
        parameter_string: str = ''
        parameter_string = ','.join(param.to_string() for param in self.parameters)
        return(f'{self.name}({parameter_string})')
