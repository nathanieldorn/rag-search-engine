from keyword_search_cli import tokenize_strings

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text):
        tokens = tokenize_strings(text)
        for token in tokens:
            if token not in self.index:
                self.index[token] = []
            self.index[token].append(doc_id)
        self.docmap[doc_id] = tokens

    def get_document(self, term):
