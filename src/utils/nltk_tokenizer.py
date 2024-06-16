import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


class NLTKTokenizer:
    def __init__(self):
        nltk.download('punkt')

    def tokenize_sentences(self, text):
        return sent_tokenize(text)

    def tokenize_words(self, text):
        return word_tokenize(text)
