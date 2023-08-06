from sqlalchemy import create_engine
from requests.auth import HTTPBasicAuth
from decouple import config
from sqlalchemy.sql.expression import text

class EdatQueriyRunner:

    @staticmethod
    def unique_result(query:str, user: str):
        connection = EdatQueriyRunner.__get_connection(user)
        return connection.execute(text(query)).one()

    @staticmethod
    def list(query:str, user: str) :
        connection = EdatQueriyRunner.__get_connection(user)
        return connection.execute(text(query)).fetchall()
    
    @staticmethod
    def __get_connection(user: str):
        engine = create_engine(
            f"trino://{config('TRINO_URL')}/{config('TRINO_CATALOG')}/{config('TRINO_SCHEMA')}",
            echo=False,
            connect_args={
                "protocol": "https",
                "requests_kwargs": {
                    "auth": HTTPBasicAuth(config("TRINO_USERNAME"), config("TRINO_PASSWD"))
                },
                "principal_username": user if user else config("TRINO_USERNAME"),
                "session_props": {"query_max_run_time": "1234m"},
            },
        )

        connection = engine.connect()
        return connection