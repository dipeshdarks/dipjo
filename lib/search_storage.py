import os
import json
import sqlite3


def _get_search_db_path(index_name):
    base = os.environ.get("DIPJO_CWD", os.getcwd())
    db_dir = os.path.join(base, ".dipjo", "data", "search")
    os.makedirs(db_dir, exist_ok=True)
    safe_name = index_name.replace("/", "_").replace("\\", "_").replace("..", "_")
    return os.path.join(db_dir, f"{safe_name}.db")


class SearchStorage:
    def __init__(self, index_name):
        self.index_name = index_name
        self.db_path = _get_search_db_path(index_name)
        self._conn = None

    def _get_conn(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def initialize(self):
        conn = self._get_conn()
        conn.execute(
            "CREATE TABLE IF NOT EXISTS documents "
            "(doc_id TEXT PRIMARY KEY, data TEXT NOT NULL)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS inverted_index "
            "(term TEXT NOT NULL, field TEXT NOT NULL, doc_ids TEXT NOT NULL, "
            "PRIMARY KEY (term, field))"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS field_lengths "
            "(doc_id TEXT NOT NULL, field TEXT NOT NULL, length INTEGER NOT NULL, "
            "PRIMARY KEY (doc_id, field))"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS metadata "
            "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        conn.commit()

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def save_document(self, doc_id, doc_data):
        conn = self._get_conn()
        data = json.dumps(doc_data, default=str)
        conn.execute(
            "INSERT OR REPLACE INTO documents (doc_id, data) VALUES (?, ?)",
            (str(doc_id), data)
        )
        conn.commit()

    def get_document(self, doc_id):
        conn = self._get_conn()
        row = conn.execute(
            "SELECT data FROM documents WHERE doc_id = ?", (str(doc_id),)
        ).fetchone()
        if row:
            return json.loads(row["data"])
        return None

    def delete_document(self, doc_id):
        conn = self._get_conn()
        conn.execute("DELETE FROM documents WHERE doc_id = ?", (str(doc_id),))
        conn.execute("DELETE FROM field_lengths WHERE doc_id = ?", (str(doc_id),))
        conn.commit()

    def get_all_documents(self):
        conn = self._get_conn()
        rows = conn.execute("SELECT doc_id, data FROM documents").fetchall()
        docs = {}
        for row in rows:
            docs[row["doc_id"]] = json.loads(row["data"])
        return docs

    def save_term(self, term, field, doc_ids):
        conn = self._get_conn()
        data = json.dumps(doc_ids)
        conn.execute(
            "INSERT OR REPLACE INTO inverted_index (term, field, doc_ids) VALUES (?, ?, ?)",
            (term, field, data)
        )
        conn.commit()

    def get_term(self, term, field=None):
        conn = self._get_conn()
        if field:
            row = conn.execute(
                "SELECT doc_ids FROM inverted_index WHERE term = ? AND field = ?",
                (term, field)
            ).fetchone()
            if row:
                return json.loads(row["doc_ids"])
            return []
        else:
            rows = conn.execute(
                "SELECT doc_ids FROM inverted_index WHERE term = ?", (term,)
            ).fetchall()
            all_ids = set()
            for row in rows:
                ids = json.loads(row["doc_ids"])
                all_ids.update(ids)
            return list(all_ids)

    def get_all_terms(self):
        conn = self._get_conn()
        rows = conn.execute("SELECT DISTINCT term FROM inverted_index").fetchall()
        return [row["term"] for row in rows]

    def delete_term(self, term, field=None):
        conn = self._get_conn()
        if field:
            conn.execute(
                "DELETE FROM inverted_index WHERE term = ? AND field = ?",
                (term, field)
            )
        else:
            conn.execute("DELETE FROM inverted_index WHERE term = ?", (term,))
        conn.commit()

    def save_field_length(self, doc_id, field, length):
        conn = self._get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO field_lengths (doc_id, field, length) VALUES (?, ?, ?)",
            (str(doc_id), field, length)
        )
        conn.commit()

    def get_field_lengths(self):
        conn = self._get_conn()
        rows = conn.execute("SELECT doc_id, field, length FROM field_lengths").fetchall()
        lengths = {}
        for row in rows:
            doc_id = row["doc_id"]
            if doc_id not in lengths:
                lengths[doc_id] = {}
            lengths[doc_id][row["field"]] = row["length"]
        return lengths

    def get_avg_field_length(self, field):
        conn = self._get_conn()
        row = conn.execute(
            "SELECT AVG(length) as avg_len FROM field_lengths WHERE field = ?", (field,)
        ).fetchone()
        return row["avg_len"] if row and row["avg_len"] else 0

    def save_metadata(self, key, value):
        conn = self._get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
            (key, json.dumps(value, default=str))
        )
        conn.commit()

    def load_metadata(self, key, default=None):
        conn = self._get_conn()
        row = conn.execute(
            "SELECT value FROM metadata WHERE key = ?", (key,)
        ).fetchone()
        if row:
            return json.loads(row["value"])
        return default

    def get_doc_count(self):
        conn = self._get_conn()
        row = conn.execute("SELECT COUNT(*) as cnt FROM documents").fetchone()
        return row["cnt"]

    def clear_all(self):
        conn = self._get_conn()
        conn.execute("DELETE FROM documents")
        conn.execute("DELETE FROM inverted_index")
        conn.execute("DELETE FROM field_lengths")
        conn.execute("DELETE FROM metadata")
        conn.commit()

    def rebuild_index(self, tokenizer, indexed_fields, field_weights):
        docs = self.get_all_documents()
        self.clear_all()

        doc_freq = {}
        for doc_id, doc_data in docs.items():
            field_tokens = {}
            for field in indexed_fields:
                value = doc_data.get(field, "")
                if isinstance(value, list):
                    value = " ".join(str(v) for v in value)
                elif not isinstance(value, str):
                    value = str(value)
                tokens = tokenizer.tokenize(value)
                field_tokens[field] = tokens
                self.save_field_length(doc_id, field, len(tokens))

            all_terms = set()
            for field, tokens in field_tokens.items():
                for term in set(tokens):
                    all_terms.add((term, field))

            for term, field in all_terms:
                term_key = f"{term}"
                if term_key not in doc_freq:
                    doc_freq[term_key] = 0
                doc_freq[term_key] += 1

        for doc_id, doc_data in docs.items():
            self.save_document(doc_id, doc_data)
            for field in indexed_fields:
                value = doc_data.get(field, "")
                if isinstance(value, list):
                    value = " ".join(str(v) for v in value)
                elif not isinstance(value, str):
                    value = str(value)
                tokens = tokenizer.tokenize(value)
                seen = {}
                for token in tokens:
                    if token not in seen:
                        seen[token] = []
                    seen[token].append(doc_id)
                for term, ids in seen.items():
                    existing = self.get_term(term, field)
                    existing_set = set(str(i) for i in existing)
                    for i in ids:
                        existing_set.add(str(i))
                    self.save_term(term, field, list(existing_set))

        self.save_metadata("doc_count", len(docs))
        self.save_metadata("field_weights", field_weights)
        self.save_metadata("indexed_fields", indexed_fields)
        return len(docs)
