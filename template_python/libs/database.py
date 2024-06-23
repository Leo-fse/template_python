import logging
import urllib.parse

from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class BaseDatabase:
    def __init__(self, db_config):
        self.host = db_config.get("host")
        self.port = db_config.get("port")
        self.user = db_config.get("user")
        self.password = db_config.get("password")
        self.Session = None  # Session attribute added

    def handle_connection_error(self, error_message):
        logger.error(f"Database connection error: {error_message}")
        # ここにエラー処理の具体的な内容を記述する

    def fetch_data(self, sql: str):
        with self.Session() as session:
            result = session.execute(sql)
            data = result.fetchall()
        return data

    def insert_data(self, sql: str):
        with self.Session() as session:
            session.execute(sql)
            session.commit()

    def update_data(self, sql: str):
        with self.Session() as session:
            session.execute(sql)
            session.commit()

    def delete_data(self, sql: str):
        with self.Session() as session:
            session.execute(sql)
            session.commit()


class OracleDatabase(BaseDatabase):
    def __init__(self, db_config):
        try:
            super().__init__(db_config)
            self.service_name = db_config.get("service_name")
            self.engine = create_engine(
                f"oracle+cx_oracle://{self.user}:{self.password}@{self.host}:{self.port}/?service_name={self.service_name}"
            )
            self.Session = sessionmaker(bind=self.engine)  # Session initialized
        except Exception as e:
            self.handle_connection_error(str(e))


class SQLServerDatabase(BaseDatabase):
    def __init__(self, db_config):
        try:
            super().__init__(db_config)
            self.database = db_config.get("database")
            self.engine = create_engine(
                f"mssql+pyodbc://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server"
            )
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            self.handle_connection_error(str(e))


class MongoDB:
    def __init__(self, db_config):
        try:
            self.host = db_config.get("host")
            self.port = db_config.get("port")
            self.user = urllib.parse.quote_plus(db_config.get("user"))
            self.password = urllib.parse.quote_plus(db_config.get("password"))
            self.database = db_config.get("database")
            self.client = MongoClient(
                f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
            self.db = self.client[self.database]
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            # ここにMongoDB用のエラー処理を記述する

    def fetch_data(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        data = collection.find(query)
        return list(data)

    def insert_data(self, collection_name: str, document: dict):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def update_data(self, collection_name: str, query: dict, update: dict):
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update})
        return result.modified_count

    def delete_data(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count
