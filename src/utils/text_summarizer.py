from summa import summarizer

from src.utils.nltk_tokenizer import NLTKTokenizer


class TextSummarizer:
    def __init__(self, tokenizer: NLTKTokenizer):
        self.tokenizer = tokenizer

    def _summarize_text(self, text, max_sentences=3, max_words=40):
        sentences = self.tokenizer.tokenize_sentences(text)
        sentences = sentences[:max_sentences]
        truncated_text = ' '.join(sentences)
        words = self.tokenizer.tokenize_words(truncated_text)
        if len(words) > max_words:
            words = words[:max_words]
            truncated_text = ' '.join(words)
            sentences = self.tokenizer.tokenize_sentences(truncated_text)
        longest_sentence = max(sentences, key=lambda s: len(self.tokenizer.tokenize_words(s)))
        return sentences, longest_sentence

    @staticmethod
    def _split(txt, seps):
        default_sep = seps[0]

        for sep in seps[1:]:
            txt = txt.replace(sep, default_sep)
        return [i.strip() for i in txt.split(default_sep) if i]

    def process_text(self, text, lang, max_sentences=7):
        n = len(self.tokenizer.tokenize_sentences(text))
        if n > max_sentences:
            if lang != "en":
                sum_text = summarizer.summarize(text, ratio=max_sentences / n, language="russian")
            else:
                sum_text = summarizer.summarize(text, ratio=max_sentences / n, language="english")
        else:
            sum_text = text

        try:
            res_s_tok, longest_sentence = self._summarize_text(sum_text)
        except Exception:
            try:
                seps = ['.', '!', '?', '', '. . .', '...']
                res_s_tok = self._split(sum_text, seps)
                if len(res_s_tok) <= 0:
                    raise Exception("No valid sentences found")
                longest_sentence = max(res_s_tok, key=len)
            except:
                raise Exception("Error processing text")

        res_s_tok.append(longest_sentence)
        return res_s_tok
