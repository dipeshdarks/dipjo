import re
import math


DEFAULT_STOP_WORDS = frozenset([
    "a", "an", "the", "and", "or", "but", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "shall", "can",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
    "into", "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "just",
    "because", "if", "about", "up", "it", "its", "this", "that", "these",
    "those", "i", "me", "my", "we", "our", "you", "your", "he", "him",
    "his", "she", "her", "they", "them", "their", "what", "which", "who",
])

_TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+(?:[_-][a-zA-Z0-9]+)*")


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


class SearchTokenizer:
    def __init__(self, stop_words=None, lowercase=True):
        if stop_words is None:
            self.stop_words = DEFAULT_STOP_WORDS
        elif stop_words is False:
            self.stop_words = frozenset()
        else:
            self.stop_words = frozenset(stop_words)
        self.lowercase = lowercase

    def tokenize(self, text):
        if not text or not isinstance(text, str):
            return []
        tokens = _TOKEN_PATTERN.findall(text)
        if self.lowercase:
            tokens = [t.lower() for t in tokens]
        tokens = [t for t in tokens if t not in self.stop_words]
        return tokens

    def tokenize_with_positions(self, text):
        if not text or not isinstance(text, str):
            return []
        results = []
        for match in _TOKEN_PATTERN.finditer(text):
            token = match.group()
            if self.lowercase:
                token = token.lower()
            if token not in self.stop_words:
                results.append((token, match.start(), match.end()))
        return results

    def compute_tf(self, tokens):
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        count = len(tokens) if tokens else 1
        for token in tf:
            tf[token] = tf[token] / count
        return tf

    def compute_idf(self, doc_freq, total_docs):
        idf = {}
        for term, freq in doc_freq.items():
            idf[term] = math.log((total_docs + 1) / (freq + 1)) + 1
        return idf

    def compute_tfidf(self, tokens, doc_freq, total_docs):
        tf = self.compute_tf(tokens)
        idf = self.compute_idf(doc_freq, total_docs)
        tfidf = {}
        for term, tf_val in tf.items():
            idf_val = idf.get(term, math.log((total_docs + 1) / 1) + 1)
            tfidf[term] = tf_val * idf_val
        return tfidf

    def compute_bm25_score(self, query_tokens, doc_tokens, avg_doc_len, k1=1.5, b=0.75):
        doc_len = len(doc_tokens)
        doc_tf = {}
        for t in doc_tokens:
            doc_tf[t] = doc_tf.get(t, 0) + 1
        score = 0.0
        for qt in query_tokens:
            if qt in doc_tf:
                tf = doc_tf[qt]
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * doc_len / avg_doc_len)
                score += numerator / denominator
        return score

    def fuzzy_match(self, token, candidates, max_distance=2):
        matches = []
        for candidate in candidates:
            dist = levenshtein_distance(token, candidate)
            if 0 < dist <= max_distance:
                matches.append((candidate, dist))
        matches.sort(key=lambda x: x[1])
        return matches
