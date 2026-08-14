import os
import json
import sqlite3


class DatabaseError(Exception):
    def __init__(self, message):
        super().__init__(f"Dipjo Database Error: {message}")


def _get_db_path():
    base = os.environ.get("DIPJO_CWD", os.getcwd())
    db_dir = os.path.join(base, ".dipjo", "data")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "dipjo.db")


class DatabaseCollection:
    def __init__(self, table_name):
        if not table_name or not isinstance(table_name, str):
            raise DatabaseError("Invalid collection name")
        self.table_name = table_name
        self.db_path = _get_db_path()
        self._conn = None
        self._ensure_table()

    def _get_conn(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _ensure_table(self):
        conn = self._get_conn()
        conn.execute(
            f"CREATE TABLE IF NOT EXISTS [{self.table_name}] "
            "(_id INTEGER PRIMARY KEY AUTOINCREMENT, _data TEXT NOT NULL)"
        )
        conn.commit()

    def _close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def create(self, record):
        if not isinstance(record, dict):
            raise DatabaseError("Invalid record: expected a dictionary")
        conn = self._get_conn()
        data = json.dumps(record)
        cursor = conn.execute(
            f"INSERT INTO [{self.table_name}] (_data) VALUES (?)", (data,)
        )
        conn.commit()
        record["id"] = cursor.lastrowid
        return record

    def find(self, filters=None):
        conn = self._get_conn()
        if filters is None or filters == {}:
            rows = conn.execute(
                f"SELECT _id, _data FROM [{self.table_name}]"
            ).fetchall()
        else:
            where_parts = []
            params = []
            for key, value in filters.items():
                if key == "id":
                    where_parts.append("_id = ?")
                    params.append(value)
                else:
                    where_parts.append(f"json_extract(_data, '$.{key}') = ?")
                    params.append(value)
            where_clause = " AND ".join(where_parts)
            rows = conn.execute(
                f"SELECT _id, _data FROM [{self.table_name}] WHERE {where_clause}",
                params,
            ).fetchall()
        results = []
        for row in rows:
            record = json.loads(row["_data"])
            record["id"] = row["_id"]
            results.append(record)
        return results

    def update(self, where, changes):
        if not isinstance(where, dict) or not isinstance(changes, dict):
            raise DatabaseError("Invalid arguments: expected dictionaries")
        conn = self._get_conn()
        existing = self.find(where)
        if not existing:
            return None
        where_parts = []
        params = []
        for key, value in where.items():
            if key == "id":
                where_parts.append("_id = ?")
                params.append(value)
            else:
                where_parts.append(f"json_extract(_data, '$.{key}') = ?")
                params.append(value)
        where_clause = " AND ".join(where_parts)
        rows = conn.execute(
            f"SELECT _id, _data FROM [{self.table_name}] WHERE {where_clause}",
            params,
        ).fetchall()
        updated_record = None
        for row in rows:
            record = json.loads(row["_data"])
            record.update(changes)
            conn.execute(
                f"UPDATE [{self.table_name}] SET _data = ? WHERE _id = ?",
                (json.dumps(record), row["_id"]),
            )
            record["id"] = row["_id"]
            updated_record = record
        conn.commit()
        return updated_record

    def delete(self, filters):
        if not isinstance(filters, dict):
            raise DatabaseError("Invalid filters: expected a dictionary")
        conn = self._get_conn()
        where_parts = []
        params = []
        for key, value in filters.items():
            if key == "id":
                where_parts.append("_id = ?")
                params.append(value)
            else:
                where_parts.append(f"json_extract(_data, '$.{key}') = ?")
                params.append(value)
        where_clause = " AND ".join(where_parts)
        cursor = conn.execute(
            f"DELETE FROM [{self.table_name}] WHERE {where_clause}", params
        )
        conn.commit()
        return {"deleted": cursor.rowcount}

    def count(self):
        conn = self._get_conn()
        row = conn.execute(
            f"SELECT COUNT(*) as cnt FROM [{self.table_name}]"
        ).fetchone()
        return row["cnt"]

    def exists(self, filters):
        results = self.find(filters)
        return len(results) > 0

    def clear(self):
        conn = self._get_conn()
        cursor = conn.execute(f"DELETE FROM [{self.table_name}]")
        conn.commit()
        return {"deleted": cursor.rowcount}
