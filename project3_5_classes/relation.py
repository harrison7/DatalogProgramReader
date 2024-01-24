import copy
from .header import Header
from .row import Row

class Relation:
    def __init__(self, name: str, header: Header, rows: set = None) -> None:
        self.name: str = name
        self.header: Header = header
        if rows is None:
            rows = set()
        self.rows: set[Row] = rows
    
    def __str__(self) -> str:
        output_str: str = ""
        for row in sorted(self.rows):
            if len(row.values) == 0:
                continue
            sep: str = ""
            output_str += "  "
            for i in range(len(self.header.values)):
                output_str += sep
                output_str += self.header.values[i]
                output_str += "="
                output_str += row.values[i]
                sep = ", "
            output_str += "\n"
        return output_str

    def to_string_row(self, row: Row) -> str:
        output_str: str = ""
        sep: str = ""
        output_str += "  "
        for i in range(len(self.header.values)):
            output_str += sep
            output_str += self.header.values[i]
            output_str += "="
            output_str += row.values[i]
            sep = ", "
        output_str += "\n"
        return output_str
        
    def add_row(self, row: Row) -> None:
        if len(row.values) != len(self.header.values):
            raise ValueError(f"Tuple is not the correct length")
        self.rows.add(row)
    
    def select1(self, value: str, col_index: int) -> 'Relation':
        if col_index >= len(self.header.values):
            raise ValueError(f"Attempting to select out of range")
        
        selected_col: str = self.header.values[col_index]
        new_name: str = self.name
        new_header: Header = self.header
        new_tuples: set[Row] = set()
        
        for row in self.rows:
            if row.values[col_index] == value:
                new_tuples.add(row)

        return Relation(new_name, new_header, new_tuples)
    
    def select2(self, index1: int, index2: int) -> 'Relation':
        if index1 >= len(self.header.values) or index2 >= len(self.header.values):
            raise ValueError(f"Attempting to select out of range")
        
        selected_col1: str = self.header.values[index1]
        selected_col2: str = self.header.values[index2]
        new_name: str = self.name
        new_header: Header = self.header
        new_tuples: set[Row] = set()
        
        for row in self.rows:
            if row.values[index1] == row.values[index2]:
                new_tuples.add(row)

        return Relation(new_name, new_header, new_tuples)
    
    def rename(self, new_header: Header) -> 'Relation':
        new_name: str = self.name

        if len(new_header.values) > len(self.header.values):
            raise ValueError(f"Attempting to rename out of range")

        while len(new_header.values) < len(self.header.values):
            new_header.values.append(self.header.values[len(new_header.values)])

            
        return Relation(new_name, new_header, copy.deepcopy(self.rows))

    def project(self, col_indexes: list[int]) -> 'Relation':
        new_name: str = self.name
        sep: str = ""
        selected_columns: list[str] = []
        for index in col_indexes:
            if index >= len(self.header.values):
                raise ValueError(f"Attempting to project out of range")
            selected_columns.append(self.header.values[index])
            # new_name += sep
            # new_name += selected_columns[-1]
            # sep = " and "

        new_header: Header = Header([self.header.values[i] for i in col_indexes])

        new_tuples: set[Row] = set()
        for row in self.rows:
            new_tuples.add(Row([row.values[i] for i in col_indexes]))

        return Relation(new_name, new_header, new_tuples)

    def natural_join(self, other: 'Relation') -> 'Relation':
        r1: Relation = self
        r2: Relation = other
        
        overlap: list[tuple(int,int)] = []
        unique_cols_1: list[int] = []
        
        for x in range(len(r1.header.values)):
            is_unique = True
            for y in range(len(r2.header.values)):
                if r1.header.values[x] == r2.header.values[y]:
                    overlap.append(tuple([x, y]))
                    is_unique = False
            if is_unique:
                unique_cols_1.append(x)

        h: Header = r1.header.join_headers(r2.header, unique_cols_1)
        result: Relation = Relation(r1.name + "|x|" + r2.name, h, set())
        for t1 in r1.rows:
            for t2 in r2.rows:
                if t1.can_join_rows(t2, overlap):
                    result_row = t1.join_rows(t2, unique_cols_1)
                    result.add_row(result_row)
        
        return result