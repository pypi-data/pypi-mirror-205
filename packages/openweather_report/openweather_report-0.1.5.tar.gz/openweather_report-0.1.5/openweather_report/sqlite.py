"""
SQLite Module
-------------

This module is to read and write to SQLite.
"""

import sys
from dataclasses import dataclass, field
from typing import Any
import aiosql
from pathlib import Path
from datetime import datetime
import json
import sqlite3


@dataclass
class DatabaseData:
    """To load and save data to sqlite."""

    connection_string: str
    entry_date: datetime
    api_call: str
    raw_data: str
    software_version: str
    query_file: str
    module_name: str
    application_name: str = "python_program"

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(
                f"{self.connection_string}",
            )
            print(f"Connection to SQLite DB successful")
        except Exception as e:
            print(f"Error {e} occurred.")

        return connection

    def load_queries(self):
        module_path = Path(sys.modules[self.module_name].__path__[0])
        return aiosql.from_path(module_path / self.query_file, "sqlite3")

    def save_json(self) -> None:
        conn = self.create_connection()
        queries = self.load_queries()
        try:
            queries.save_json_data_no_schema(
                conn,
                entry_date=self.entry_date,
                api_call=self.api_call,
                raw_data=self.raw_data,
                software_version=self.software_version,
            )
            print("Data saved.")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error {e} occurred.")
