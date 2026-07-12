class TableComponent:
    def __init__(self, headers: list, rows: list):
        self.headers = headers
        self.rows = rows
    def to_dict(self) -> dict:
        return {"type": "table", "headers": self.headers, "rows": self.rows}
