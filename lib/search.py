import re
import time
import math
from datetime import datetime
from search_tokenizer import SearchTokenizer, levenshtein_distance
from search_storage import SearchStorage


class SearchError(Exception):
    def __init__(self, message):
        super().__init__(f"DipjoSearch Error: {message}")


_DEFAULT_FIELDS = ["title", "content", "description", "tags"]
_DEFAULT_WEIGHTS = {"title": 3, "tags": 2, "content": 1, "description": 1}


class SearchIndex:
    def __init__(self, name, indexed_fields=None, field_weights=None,
                 stop_words=None, use_bm25=False):
        self.name = name
        self.indexed_fields = indexed_fields or list(_DEFAULT_WEIGHTS.keys())
        self.field_weights = dict(field_weights) if field_weights else dict(_DEFAULT_WEIGHTS)
        for f in self.indexed_fields:
            if f not in self.field_weights:
                self.field_weights[f] = 1
        self.use_bm25 = use_bm25
        self.tokenizer = SearchTokenizer(stop_words=stop_words)
        self.storage = SearchStorage(name)
        self.storage.initialize()
        self._pending_adds = {}
        self._pending_updates = {}
        self._pending_deletes = set()
        self._doc_freq_cache = {}
        self._doc_count_cache = 0
        self._load_caches()

    def _load_caches(self):
        self._doc_count_cache = self.storage.get_doc_count()
        self._rebuild_doc_freq()

    def _rebuild_doc_freq(self):
        self._doc_freq_cache = {}
        for term in self.storage.get_all_terms():
            ids = self.storage.get_term(term)
            self._doc_freq_cache[term] = len(ids)

    def add(self, doc):
        if not isinstance(doc, dict):
            raise SearchError("Document must be a dictionary")
        doc_id = str(doc.get("id", ""))
        if not doc_id:
            raise SearchError("Document must have an 'id' field")
        self._pending_adds[doc_id] = doc
        return self

    def update(self, doc):
        if not isinstance(doc, dict):
            raise SearchError("Document must be a dictionary")
        doc_id = str(doc.get("id", ""))
        if not doc_id:
            raise SearchError("Document must have an 'id' field")
        self._pending_updates[doc_id] = doc
        return self

    def delete(self, doc_id):
        self._pending_deletes.add(str(doc_id))
        return self

    def get(self, doc_id):
        return self.storage.get_document(str(doc_id))

    def count(self):
        return self._doc_count_cache

    def clear(self):
        self._pending_adds.clear()
        self._pending_updates.clear()
        self._pending_deletes.clear()
        self.storage.clear_all()
        self._doc_freq_cache.clear()
        self._doc_count_cache = 0
        return self

    def commit(self):
        for doc_id, doc in self._pending_updates.items():
            existing = self.storage.get_document(doc_id)
            if existing:
                existing.update(doc)
                self.storage.save_document(doc_id, existing)
            else:
                self.storage.save_document(doc_id, doc)

        for doc_id, doc in self._pending_adds.items():
            if doc_id in self._pending_deletes:
                continue
            self.storage.save_document(doc_id, doc)

        for doc_id in self._pending_deletes:
            self.storage.delete_document(doc_id)

        self._pending_adds.clear()
        self._pending_updates.clear()
        self._pending_deletes.clear()

        self._rebuild_doc_freq()
        self._rebuild_field_index()
        self._doc_count_cache = self.storage.get_doc_count()
        self.storage.save_metadata("doc_count", self._doc_count_cache)
        self.storage.save_metadata("indexed_fields", self.indexed_fields)
        self.storage.save_metadata("field_weights", self.field_weights)
        return self

    def _rebuild_field_index(self):
        docs = self.storage.get_all_documents()
        for field in self.indexed_fields:
            term_docs = {}
            for doc_id, doc_data in docs.items():
                value = doc_data.get(field, "")
                if isinstance(value, list):
                    value = " ".join(str(v) for v in value)
                elif not isinstance(value, str):
                    value = str(value)
                tokens = self.tokenizer.tokenize(value)
                self.storage.save_field_length(doc_id, field, len(tokens))
                seen = set()
                for token in tokens:
                    if token not in seen:
                        seen.add(token)
                        if token not in term_docs:
                            term_docs[token] = []
                        term_docs[token].append(doc_id)
            for term, ids in term_docs.items():
                self.storage.save_term(term, field, ids)

    def search(self, query, options=None):
        if options is None:
            options = {}
        start_time = time.time()

        limit = options.get("limit", 20)
        offset = options.get("offset", 0)
        filters = options.get("filter", {})
        sort_by = options.get("sort", "score")
        sort_order = options.get("order", "desc")
        highlight = options.get("highlight", True)
        fuzzy = options.get("fuzzy", False)
        fuzzy_distance = options.get("fuzzy_distance", 2)
        ranking = options.get("ranking", "bm25" if self.use_bm25 else "tfidf")

        parsed = self._parse_query(query)
        candidate_ids = self._get_candidates(parsed)
        scored = self._score_documents(parsed, candidate_ids, ranking)

        if filters:
            scored = self._apply_filters(scored, filters)

        scored = self._sort_results(scored, sort_by, sort_order)
        total = len(scored)

        page = scored[offset:offset + limit]

        results = []
        for doc_id, score in page:
            doc = self.storage.get_document(doc_id)
            if doc is None:
                continue
            result = {"score": round(score, 4), "document": doc}
            if highlight:
                result["highlights"] = self._highlight_doc(doc, parsed)
            results.append(result)

        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "query": query,
            "total": total,
            "time_ms": elapsed_ms,
            "results": results,
        }

    def suggest(self, prefix, max_results=10):
        if not prefix or not isinstance(prefix, str):
            return []
        prefix_lower = prefix.lower()
        all_terms = self.storage.get_all_terms()
        matches = []
        for term in all_terms:
            if term.startswith(prefix_lower):
                matches.append(term)
        matches.sort()
        return matches[:max_results]

    def stats(self):
        docs = self.storage.get_all_documents()
        all_terms = self.storage.get_all_terms()
        total_tokens = 0
        for doc_id, doc_data in docs.items():
            for field in self.indexed_fields:
                value = doc_data.get(field, "")
                if isinstance(value, list):
                    value = " ".join(str(v) for v in value)
                elif not isinstance(value, str):
                    value = str(value)
                total_tokens += len(self.tokenizer.tokenize(value))

        avg_doc_len = total_tokens / len(docs) if docs else 0
        try:
            import os
            db_path = self.storage.db_path
            index_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        except Exception:
            index_size = 0

        return {
            "documents": len(docs),
            "unique_terms": len(all_terms),
            "indexed_fields": self.indexed_fields,
            "index_size": index_size,
            "average_document_length": round(avg_doc_len, 2),
        }

    def rebuild(self):
        count = self.storage.rebuild_index(
            self.tokenizer, self.indexed_fields, self.field_weights
        )
        self._doc_count_cache = count
        self._rebuild_doc_freq()
        return count

    def save(self):
        self.commit()
        return self

    def load(self):
        self._load_caches()
        return self

    def close(self):
        self.commit()
        self.storage.close()

    # -- Query Parser --

    def _parse_query(self, query):
        if not query or not isinstance(query, str):
            return {"type": "empty"}
        tokens = self._tokenize_query(query)
        if not tokens:
            return {"type": "empty"}
        return self._parse_or(tokens, 0)

    def _tokenize_query(self, query):
        tokens = []
        i = 0
        while i < len(query):
            if query[i] in " \t":
                i += 1
                continue
            if query[i] == '"':
                j = i + 1
                while j < len(query) and query[j] != '"':
                    j += 1
                phrase = query[i + 1:j]
                if j < len(query):
                    j += 1
                tokens.append(("PHRASE", phrase))
                i = j
            elif query[i:i + 5].lower() == "not " and (i == 0 or query[i - 1] in " \t"):
                tokens.append(("OP", "NOT"))
                i += 4
            elif query[i:i + 4].lower() == "and " and (i == 0 or query[i - 1] in " \t"):
                tokens.append(("OP", "AND"))
                i += 4
            elif query[i:i + 3].lower() == "or " and (i == 0 or query[i - 1] in " \t"):
                tokens.append(("OP", "OR"))
                i += 3
            elif query[i:i + 4].lower() == "not" and i + 4 >= len(query):
                tokens.append(("OP", "NOT"))
                i += 3
            elif query[i:i + 3].lower() == "and" and i + 3 >= len(query):
                tokens.append(("OP", "AND"))
                i += 3
            elif query[i:i + 2].lower() == "or" and i + 2 >= len(query):
                tokens.append(("OP", "OR"))
                i += 2
            else:
                j = i
                while j < len(query) and query[j] not in ' \t"':
                    j += 1
                word = query[i:j]
                i = j
                if ":" in word and not word.startswith('"'):
                    parts = word.split(":", 1)
                    field_name = parts[0].lower()
                    term_value = parts[1]
                    tokens.append(("FIELD", (field_name, term_value)))
                else:
                    tokens.append(("TERM", word))
        return tokens

    def _parse_or(self, tokens, pos):
        left = self._parse_and(tokens, pos)
        while pos < len(tokens) and tokens[pos] == ("OP", "OR"):
            pos += 1
            right = self._parse_and(tokens, pos)
            left = {"type": "or", "left": left, "right": right}
        return left

    def _parse_and(self, tokens, pos):
        left = self._parse_not(tokens, pos)
        while pos < len(tokens) and tokens[pos] == ("OP", "AND"):
            pos += 1
            right = self._parse_not(tokens, pos)
            left = {"type": "and", "left": left, "right": right}
        return left

    def _parse_not(self, tokens, pos):
        if pos < len(tokens) and tokens[pos] == ("OP", "NOT"):
            pos += 1
            operand = self._parse_primary(tokens, pos)
            return {"type": "not", "operand": operand}
        return self._parse_primary(tokens, pos)

    def _parse_primary(self, tokens, pos):
        if pos >= len(tokens):
            return {"type": "empty"}
        token = tokens[pos]
        if token[0] == "TERM":
            return {"type": "term", "value": token[1].lower()}
        elif token[0] == "PHRASE":
            phrase_tokens = self.tokenizer.tokenize(token[1])
            return {"type": "phrase", "tokens": phrase_tokens, "raw": token[1]}
        elif token[0] == "FIELD":
            field_name, term_value = token[1]
            return {"type": "field", "field": field_name, "value": term_value.lower()}
        return {"type": "empty"}

    # -- Candidate Retrieval --

    def _get_candidates(self, parsed):
        docs = self.storage.get_all_documents()
        if not docs:
            return set()
        return self._collect_candidates(parsed, set(docs.keys()))

    def _collect_candidates(self, parsed, all_ids):
        ptype = parsed.get("type")
        if ptype == "empty":
            return all_ids
        if ptype == "term":
            term = parsed["value"]
            ids = set(str(i) for i in self.storage.get_term(term))
            return ids & all_ids
        if ptype == "phrase":
            return all_ids
        if ptype == "field":
            field = parsed["field"]
            value = parsed["value"]
            ids = set(str(i) for i in self.storage.get_term(value, field=field))
            return ids & all_ids
        if ptype == "and":
            left = self._collect_candidates(parsed["left"], all_ids)
            right = self._collect_candidates(parsed["right"], all_ids)
            return left & right
        if ptype == "or":
            left = self._collect_candidates(parsed["left"], all_ids)
            right = self._collect_candidates(parsed["right"], all_ids)
            return left | right
        if ptype == "not":
            operand = self._collect_candidates(parsed["operand"], all_ids)
            return all_ids - operand
        return all_ids

    # -- Scoring --

    def _score_documents(self, parsed, candidate_ids, ranking):
        docs = self.storage.get_all_documents()
        total_docs = len(docs) if docs else 1
        scores = {}
        doc_freq = self._doc_freq_cache

        for doc_id in candidate_ids:
            doc = docs.get(doc_id)
            if doc is None:
                continue
            score = self._score_single(doc_id, doc, parsed, total_docs, doc_freq, ranking)
            if score > 0:
                scores[doc_id] = score
        return scores

    def _score_single(self, doc_id, doc, parsed, total_docs, doc_freq, ranking):
        ptype = parsed.get("type")
        if ptype == "empty":
            return 0
        if ptype == "term":
            return self._score_term(doc_id, doc, parsed["value"], total_docs, doc_freq, ranking)
        if ptype == "phrase":
            return self._score_phrase(doc_id, doc, parsed["tokens"])
        if ptype == "field":
            return self._score_field_term(doc_id, doc, parsed["field"], parsed["value"], total_docs, doc_freq, ranking)
        if ptype == "and":
            left = self._score_single(doc_id, doc, parsed["left"], total_docs, doc_freq, ranking)
            right = self._score_single(doc_id, doc, parsed["right"], total_docs, doc_freq, ranking)
            if left > 0 and right > 0:
                return left + right
            return 0
        if ptype == "or":
            left = self._score_single(doc_id, doc, parsed["left"], total_docs, doc_freq, ranking)
            right = self._score_single(doc_id, doc, parsed["right"], total_docs, doc_freq, ranking)
            return max(left, right)
        if ptype == "not":
            return 1.0 if self._score_single(doc_id, doc, parsed["operand"], total_docs, doc_freq, ranking) == 0 else 0
        return 0

    def _score_term(self, doc_id, doc, term, total_docs, doc_freq, ranking):
        total_score = 0.0
        for field in self.indexed_fields:
            weight = self.field_weights.get(field, 1)
            value = doc.get(field, "")
            if isinstance(value, list):
                value = " ".join(str(v) for v in value)
            elif not isinstance(value, str):
                value = str(value)
            tokens = self.tokenizer.tokenize(value)
            if ranking == "bm25":
                avg_len = self.storage.get_avg_field_length(field) or 1
                score = self.tokenizer.compute_bm25_score([term], tokens, avg_len)
            else:
                tfidf = self.tokenizer.compute_tfidf(tokens, doc_freq, total_docs)
                score = tfidf.get(term, 0)
            total_score += score * weight
        return total_score

    def _score_phrase(self, doc_id, doc, phrase_tokens):
        if not phrase_tokens:
            return 0
        total_score = 0.0
        for field in self.indexed_fields:
            weight = self.field_weights.get(field, 1)
            value = doc.get(field, "")
            if isinstance(value, list):
                value = " ".join(str(v) for v in value)
            elif not isinstance(value, str):
                value = str(value)
            tokens = self.tokenizer.tokenize(value)
            phrase_len = len(phrase_tokens)
            for i in range(len(tokens) - phrase_len + 1):
                window = tokens[i:i + phrase_len]
                if window == phrase_tokens:
                    total_score += weight * 10.0
                    break
        return total_score

    def _score_field_term(self, doc_id, doc, field, term, total_docs, doc_freq, ranking):
        if field not in self.indexed_fields:
            return 0
        weight = self.field_weights.get(field, 1)
        value = doc.get(field, "")
        if isinstance(value, list):
            value = " ".join(str(v) for v in value)
        elif not isinstance(value, str):
            value = str(value)
        tokens = self.tokenizer.tokenize(value)
        if ranking == "bm25":
            avg_len = self.storage.get_avg_field_length(field) or 1
            score = self.tokenizer.compute_bm25_score([term], tokens, avg_len)
        else:
            tfidf = self.tokenizer.compute_tfidf(tokens, doc_freq, total_docs)
            score = tfidf.get(term, 0)
        return score * weight

    # -- Filtering --

    def _apply_filters(self, scores, filters):
        filtered = {}
        for doc_id, score in scores.items():
            doc = self.storage.get_document(doc_id)
            if doc is None:
                continue
            match = True
            for key, value in filters.items():
                doc_val = doc.get(key)
                if isinstance(doc_val, list):
                    if value not in doc_val:
                        match = False
                        break
                elif doc_val != value:
                    match = False
                    break
            if match:
                filtered[doc_id] = score
        return filtered

    # -- Sorting --

    def _sort_results(self, scores, sort_by, sort_order):
        items = list(scores.items())
        if sort_by == "score":
            items.sort(key=lambda x: x[1], reverse=(sort_order == "desc"))
        else:
            def sort_key(item):
                doc = self.storage.get_document(item[0])
                if doc is None:
                    return ""
                val = doc.get(sort_by, "")
                if isinstance(val, (int, float)):
                    return val
                return str(val)
            items.sort(key=sort_key, reverse=(sort_order == "desc"))
        return items

    # -- Highlighting --

    def _highlight_doc(self, doc, parsed):
        highlights = {}
        query_terms = self._extract_query_terms(parsed)
        for field in self.indexed_fields:
            value = doc.get(field, "")
            if isinstance(value, list):
                value = " ".join(str(v) for v in value)
            elif not isinstance(value, str):
                value = str(value)
            if not value:
                continue
            highlighted = self._highlight_text(value, query_terms)
            if highlighted != value:
                highlights[field] = highlighted
        return highlights

    def _extract_query_terms(self, parsed):
        terms = []
        ptype = parsed.get("type")
        if ptype == "term":
            terms.append(parsed["value"])
        elif ptype == "phrase":
            terms.extend(parsed["tokens"])
        elif ptype == "field":
            terms.append(parsed["value"])
        elif ptype == "and":
            terms.extend(self._extract_query_terms(parsed["left"]))
            terms.extend(self._extract_query_terms(parsed["right"]))
        elif ptype == "or":
            terms.extend(self._extract_query_terms(parsed["left"]))
            terms.extend(self._extract_query_terms(parsed["right"]))
        elif ptype == "not":
            terms.extend(self._extract_query_terms(parsed["operand"]))
        return terms

    def _highlight_text(self, text, query_terms):
        if not query_terms:
            return text
        result = text
        for term in sorted(query_terms, key=len, reverse=True):
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            result = pattern.sub(lambda m: f"<mark>{m.group()}</mark>", result)
        return result

    # -- Fuzzy Search --

    def fuzzy_search(self, query, options=None):
        if options is None:
            options = {}
        max_distance = options.get("fuzzy_distance", 2)
        fuzzy_tokens = []
        parsed = self._parse_query(query)
        query_terms = self._extract_query_terms(parsed)
        all_terms = self.storage.get_all_terms()
        for qt in query_terms:
            matches = self.tokenizer.fuzzy_match(qt, all_terms, max_distance)
            if matches:
                for match_term, dist in matches:
                    fuzzy_tokens.append(match_term)
            else:
                fuzzy_tokens.append(qt)
        fuzzy_query = " ".join(fuzzy_tokens)
        return self.search(fuzzy_query, options)

    # -- List all indexes --

    @staticmethod
    def list_indexes():
        import os
        base = os.environ.get("DIPJO_CWD", os.getcwd())
        search_dir = os.path.join(base, ".dipjo", "data", "search")
        if not os.path.isdir(search_dir):
            return []
        indexes = []
        for f in os.listdir(search_dir):
            if f.endswith(".db"):
                indexes.append(f[:-3])
        return sorted(indexes)

    @staticmethod
    def delete_index(name):
        import os
        base = os.environ.get("DIPJO_CWD", os.getcwd())
        db_path = os.path.join(base, ".dipjo", "data", "search", f"{name}.db")
        if os.path.exists(db_path):
            os.remove(db_path)
            return True
        return False
