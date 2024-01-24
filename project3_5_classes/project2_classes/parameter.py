class Parameter():
    def __init__(self, value: str, is_id: bool):
        self.value = value
        self.is_id = is_id

    def to_string(self) -> str:
        return self.value