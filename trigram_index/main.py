from collections import defaultdict
from typing import NamedTuple, Dict, List, Tuple

DocID = int


class IndexResult(NamedTuple):
    freq: Dict[DocID, int]
    docs_ids: Dict[DocID, bool]


class NgramIndex:
    mapping: Dict[str, IndexResult]
    docs: Dict[DocID, str]

    def __init__(self):
        self.mapping = {}
        self.docs = {}

    def _tokenize(self, text: str) -> List[str]:
        for i in range(len(text) - 2):
            yield text[i:i + 3]

    def add(self, doc_id: int, text: str):
        for token in self._tokenize(text):
            index_result = self.mapping.get(token)
            if index_result is None:
                self.mapping[token] = index_result = IndexResult({}, {})

            index_result.docs_ids[doc_id] = True
            index_result.freq[doc_id] = index_result.freq.get(doc_id, 0) + 1

        self.docs[doc_id] = text

    def search(self, text: str) -> List[Tuple[str, float]]:
        tokens = self._tokenize(text)

        scoring = defaultdict(int)
        for token in tokens:
            index_result = self.mapping.get(token)
            if not index_result:
                continue
            for doc_id in index_result.docs_ids:
                # very simple scoring algorithm
                scoring[doc_id] += 1 + index_result.freq[doc_id] / 2

        return [(self.docs[doc_id], score / len(self.docs[doc_id])) for doc_id, score in scoring.items()]


def run():
    index = NgramIndex()

    index.add(1, 'mazerunner')
    index.add(2, 'amazing')
    index.add(3, 'running')

    print(list(sorted(index.search('amaz'), key=lambda x: x[1], reverse=True))[:5])
