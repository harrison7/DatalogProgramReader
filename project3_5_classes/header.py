class Header:
    def __init__(self, values: list[str]) -> None:
        self.values: list[str] = values

    def join_headers(self, other: 'Header', unique_cols_1: list[int]) -> 'Header':
        header1: Row = self
        header2: Row = other
        
        new_header_values: list[str] = []
        for x in unique_cols_1:
            new_header_values.append(header1.values[x])
        new_header_values.extend(header2.values)
        
        return Header(new_header_values)
    