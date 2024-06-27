from sqlalchemy import create_engine, Engine


class PostgresConnection:
    engine: Engine

    def __init__(
            self,
            db_url: str,
    ):
        self.engine = create_engine(db_url)
