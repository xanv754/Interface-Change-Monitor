from data.libs.database import Database


class Query:
    """Class to manage query."""
    database: Database

    def __init__(self, uri: str | None = None):
        self.database = Database(uri=uri)