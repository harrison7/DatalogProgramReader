import os

from project3_5_classes.project2_classes.project1_classes.token import Token
from project3_5_classes.project2_classes.project1_classes.lexer import Lexer

from project3_5_classes.project2_classes.parser import Parser

from project3_5_classes.relation import Relation
from project3_5_classes.header import Header
from project3_5_classes.row import Row
from project3_5_classes.interpreter import Interpreter

#Return your program output here for grading (can treat this function as your "main")
def project5(input: str) -> str:
    lexer: Lexer = Lexer()
    lexer.run(input)
    tokens: list[Token] = lexer.get_tokens()

    parser: Parser = Parser()
    parser.run(tokens)
    datalog_program: DatalogProgram = parser.datalog_program

    interpreter: Interpreter = Interpreter()
    return interpreter.run(datalog_program)

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("project5-passoff/80/input6.txt")
    print(project5(input_contents))
