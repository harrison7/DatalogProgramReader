# this is sometimes called tuple, I am renaming it to help be specific
class Row:
    def __init__(self, values: list[str]) -> None:
        self.values: list[str] = values
    
    def __eq__(self, other: 'Row') -> bool:
        return self.values == other.values
    
    def __hash__(self) -> int:
        return hash(tuple(self.values))
    
    def __lt__(self, other: 'Row') -> bool:
        return self.values < other.values

    def can_join_rows(self, other: 'Row', overlap: list[tuple[int,int]]) -> bool:
        row1: Row = self
        row2: Row = other

        for x, y in overlap:
            if row1.values[x] != row2.values[y]:
                return False

        return True
        
    def join_rows(self, other: 'Row', unique_cols_1: list[int]) -> 'Row':
        row1: Row = self
        row2: Row = other
        
        new_row_values: list[str] = []
        for x in unique_cols_1:
            new_row_values.append(row1.values[x])
        new_row_values.extend(row2.values)
        
        return Row(new_row_values)