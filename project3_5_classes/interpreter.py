import copy
from .relation import Relation
from .row import Row
from .header import Header
from .database import Database
from .graph import Graph
from typing import Dict

from .project2_classes.project1_classes.token import Token
from .project2_classes.project1_classes.lexer import Lexer

from .project2_classes.parser import Parser
from .project2_classes.datalog_program import DatalogProgram
from .project2_classes.predicate import Predicate
from .project2_classes.rule import Rule

class Interpreter:
    def __init__(self) -> None:
        self.output_str: str = ""
        self.database: Database = Database()
        self.constants: dict[str, int] = {}
        self.changed: bool = False
    
    def run(self, datalog_program: DatalogProgram) -> str:
        self.datalog_program: DatalogProgram = datalog_program
        self.constants = {}
        self.interpret_schemes()
        self.interpret_facts()
        self.interpret_rules()
        self.interpret_queries()
        return self.output_str
        # return str(self.database.database)
    
    def interpret_schemes(self) -> None:
        # Start with an empty Database. 
        self.database.reset()
        # For each scheme in the Datalog program, 
        #   add an empty Relation to the Database. 
        #   Use the scheme name as the name of the relation 
        #   and the attribute list from the scheme as the header of the relation.
        for scheme in self.datalog_program.schemes:
            scheme_attributes: list[str] = []
            for attribute in scheme.parameters:
                scheme_attributes.append(attribute.to_string())
            scheme_header: Header = Header(scheme_attributes)
            scheme_relation: Relation = Relation(scheme.name, scheme_header)
            self.database.add_relation(scheme.name, scheme_relation)
        pass
    
    def interpret_facts(self) -> None:
        # For each fact in the Datalog program, 
        #   add a Tuple to a Relation. 
        #   Use the predicate name from the fact to 
        #   determine the Relation to which the Tuple should be added. 
        #   Use the values listed in the fact to provide the values for the Tuple.
        for fact in self.datalog_program.facts:
            fact_attributes: list[str] = []
            for attribute in fact.parameters:
                fact_attributes.append(attribute.to_string())
            fact_row: Row = Row(fact_attributes)
            self.database.get_relation(fact.name).add_row(fact_row)
        pass
    
    def interpret_queries(self) -> None:
        # for each query in the datalog_program call evaluate predicate.
            # append the predicate returned by this function to the output string
            
        # output notes:
        # For each query, output the query and a space. 
        # If the relation resulting from evaluating the query is empty, output 'No'. 
        # If the resulting relation is not empty, output 'Yes(n)' where n is the number of tuples in the resulting relation.
        
        # If there are variables in the query, output the tuples from the resulting relation.

        # Output each tuple on a separate line as a comma-space-separated list of pairs.
        # Each pair has the form N='V', 
        # where N is the attribute name from the header and V is the value from the tuple. 
        # Output the name-value pairs in the same order as the variable names appear in the query. 
        # Indent the output of each tuple by two spaces.
        
        # some of this output code was given to you in the Relation.__str__() function. 
        # It may need to be modified slightly

        # Output the tuples in sorted order. 
        # Sort the tuples alphabetically based on the values in the tuples. 
        # Sort first by the value in the first position and if needed up to the value in the nth position.
        
        self.output_str += "Query Evaluation\n"

        for query in self.datalog_program.queries:
            self.constants = {}
            self.output_str += query.to_string()
            self.output_str += "? "
            self.evaluate_predicate(query, True)

        pass
    
    def evaluate_predicate(self, predicate: Predicate, checkQuery: bool) -> Relation:
        # For this predicate you need to
        #   use a sequence of select, project, and rename operations on the Database 
        #   to evaluate the query. Evaluate the queries in the order given in the input.
        # Get the Relation from the Database with the 
        #   same name as the predicate name in the query.
        # Use one or more select operations to select 
        #   the tuples from the Relation that match the query. Iterate over the parameters of the query: If the parameter is a constant, select the tuples from the Relation that have the same value as the constant in the same position as the constant. If the parameter is a variable and the same variable name appears later in the query, select the tuples from the Relation that have the same value in both positions where the variable name appears.
        # After selecting the matching tuples, use the project operation 
        #   to keep only the columns from the Relation that correspond to the 
        #   positions of the variables in the query. Make sure that each variable name appears only once in the resulting relation. If the same name appears more than once, keep the first column where the name appears and remove any later columns where the same name appears. (This makes a difference when there are other columns in between the ones with the same name.)
        # After projecting, use the rename operation to 
        #   rename the header of the Relation to the
        #   names of the variables found in the query.
        # The operations must be done in the order described above: 
        #   any selects, 
        #   followed by a project, 
        #   followed by a rename.
        # return the new predicate

        new_relation: Relation = copy.deepcopy(self.database.database[predicate.name])

        index: int = 0
        no_constants: bool = True
        for parameter in predicate.parameters:
            if parameter.is_id:
                no_constants = False
                if parameter.value in self.constants:
                    new_relation = new_relation.select2(self.constants[parameter.value], index)
                else:
                    self.constants[parameter.value] = index
            else:
                new_relation = new_relation.select1(parameter.value, index)
            
            index += 1

        if len(new_relation.rows) == 0:
            if checkQuery:
                self.output_str += "No\n"
        else:
            if checkQuery:
                self.output_str += "Yes("
                self.output_str += str(len(new_relation.rows))
                self.output_str += ")\n"
            if not no_constants:
                new_relation = new_relation.project(self.constants.values())
                new_relation = new_relation.rename(Header(list(self.constants.keys())))
            else:
                new_relation = new_relation.project([])
            if checkQuery:
                self.output_str += new_relation.__str__()
                
        return new_relation
    
    # this will be implemented during project 4
    def interpret_rules(self) -> None:

        # make the giant joinRelation
        # project, rename
        # print out all unique tuples: check each tuple by unioning with main relation, 
        # check size before and after to see if its unique
        # union unique cells to database
        # repeat until no unique cells are added

        # fixed point algorithm to evaluate rules goes here:

        graph: Graph = Graph(self.datalog_program.rules)
        self.output_str += "Dependency Graph\n"
        for node in graph.graph:
            self.output_str += "R"
            self.output_str += str(node)
            self.output_str += ":"
            sep: str = ""
            for dependency in graph.graph[node]:
                self.output_str += sep
                self.output_str += "R"
                self.output_str += str(dependency)
                sep = ","
            self.output_str += "\n"

        self.output_str += "\nRule Evaluation\n"
        for scc in graph.scc:
            new_rows: int = 0
            rule_passes: int = 0
            self.output_str += "SCC: "
            self.output_str += self.scc_string(scc)

            loop_once: bool = False
            
            self.changed = True
            while self.changed and not loop_once:
                self.changed = False
                for index in sorted(scc):
                    rule: Rule = self.datalog_program.rules[index]

                    set_loop_flag: bool = True
                    if len(scc) == 1:
                        for predicate in rule.body_predicates:
                            if predicate.name == rule.head_predicate.name:
                                set_loop_flag = False
                                break
                        if set_loop_flag:
                            loop_once = True

                    self.constants = {}
                    self.output_str += rule.to_string()
                    self.output_str += ".\n"
                    new_rows += self.evaluate_rule(rule)
                rule_passes += 1

            self.output_str += str(rule_passes)
            self.output_str += " passes: "
            self.output_str += self.scc_string(scc)

        self.output_str += "\n"

    # this function should return the number of unique tuples added to the database
    def evaluate_rule(self, rule: Rule) -> int:
        # Step 1:
        
        # Evaluate the predicates on the right-hand side of the rule (the body predicates):

        # For each predicate on the right-hand side of a rule, 
        #   evaluate the predicate in the same way you evaluated the queries in the last project (using select, project, and rename operations). 
        #   Each predicate should produce a single relation as an intermediate result. 
        #   If there are n predicates on the right-hand side of a rule, 
        #   there should be n intermediate results.
        
        # HINT: 
        #   if you used the EvaluatePredicate function as suggested in lab 3
        #   you should only need to call that function once per 
        #   body predicate and store the result
        rule_name: str = rule.head_predicate.name
        original_relation: Relation = self.database.database[rule_name]

        relation_list: list[Relation] = []

        for predicate in rule.body_predicates:
            self.constants = {}
            pred_relation: Relation = self.evaluate_predicate(predicate, False)
            relation_list.append(pred_relation)
        
        # Example:
        # for body_predicate in rule.body:
        # result = self.evaluate_predicate(body_predicate))

        # Step 2:
        # Join the relations that result:

        # If there are two or more predicates on the right-hand side of a rule, 
        #   join the intermediate results to form the single result for Step 2. 
        #   Thus, if p1, p2, and p3 are the intermediate results from Step 1, join them 
        #   (p1 |x| p2 |x| p3) into a single relation.

        # If there is a single predicate on the right hand side of the rule, 
        # use the single intermediate result from Step 1 as the result for Step 2.

        new_relation: Relation = relation_list[0]

        for relation in range(len(relation_list) - 1):
            new_relation = new_relation.natural_join(relation_list[relation + 1])

        # Step 3:
        # Project the columns that appear in the head predicate:

        # The predicates in the body of a rule may have variables 
        #   that are not used in the head of the rule. 
        #   The variables in the head may also appear in a different order 
        #   than those in the body. Use a project operation on the result from 
        #   Step 2 to remove the columns that don't appear in the head of the 
        #   rule and to reorder the columns to match the order in the head.

        predicate_length: int = len(rule.head_predicate.parameters)
        project_index: list[int] = [None] * predicate_length

        i_index: int = 0
        j_index: int = 0
        for i in new_relation.header.values:
            j_index = 0
            for j in rule.head_predicate.parameters:
                if i == j.value:
                    project_index[j_index] = i_index
                j_index += 1
            i_index += 1

        new_relation = new_relation.project(project_index)
        # print(new_relation.__str__())

        # Step 4:
        # Rename the relation to make it union-compatible:
        
        # Rename the relation that results from Step 3 to 
        #   make it union compatible with the relation that 
        #   matches the head of the rule. Rename each attribute 
        #   in the result from Step 3 to the attribute name found 
        #   in the corresponding position in the relation 
        #   that matches the head of the rule.

        rename_list: list[str] = []
        for column in original_relation.header.values:
            rename_list.append(column)

        renamed_header = Header(rename_list)
        new_relation = new_relation.rename(renamed_header)
        # print(new_relation.__str__())

        # Step 5:
        # Union with the relation in the database:

        # Save the size of the database relation before calling union
        scheme_length: int = len(original_relation.rows)
        size_before: int = scheme_length

        # Union the result from Step 4 with the relation 
        # in the database whose name matches the name of the head of the rule.

        for row in sorted(new_relation.rows):
            original_relation.add_row(row)
            new_length = len(original_relation.rows)
            if new_length > scheme_length:
                original_relation.add_row(row)
                self.changed = True
                scheme_length = new_length
                self.output_str += new_relation.to_string_row(row)
        
        # Save the size of the database relation after calling union
        size_after: int = len(original_relation.rows)
        
        return size_after - size_before

    def scc_string(self, scc: set[int]) -> str:
        output_str: str = ""
        sep: str = ""
        for rule in scc:
            output_str += sep
            output_str += "R"
            output_str += str(rule)
            sep = ","
        output_str += "\n"
        return output_str