import random
import string
from dataclasses import dataclass
from itertools import zip_longest

import nltk
from nltk import Text
from textstat import textstat

from grammarcheck.language_service import NLTKLanguageService


@dataclass
class TaggedText:
    id: str
    text: str
    tags: list[tuple[str, str]]
    level: float = 0.0


@dataclass
class TagAttemptResult:
    score: int
    results: list[tuple[str, bool]]


class TaggedTextRepository:
    def __init__(self):
        self.tagged_text = {}

    def add(self, tagged_text: TaggedText):
        self.tagged_text[tagged_text.id] = tagged_text

    def get_all(self) -> list[TaggedText]:
        return list(self.tagged_text.values())

    def get(self, text_id: str) -> TaggedText:
        return self.tagged_text.get(text_id)


class IncrementalIdGenerator:
    def __init__(self):
        self.id = 0

    def generate_id(self) -> str:
        self.id += 1
        return str(self.id)


class PosFacade:
    def __init__(self):
        self.language_service = NLTKLanguageService()
        self.id_generator = IncrementalIdGenerator()
        self.tagged_text_repository = TaggedTextRepository()

    def add_raw_text(self, text: str) -> TaggedText:
        tagged_text = TaggedText(
            self.id_generator.generate_id(),
            text, self.language_service.pos_tag(text),
            textstat.flesch_reading_ease(text))
        self.tagged_text_repository.add(tagged_text)
        return tagged_text

    def get_random_tagged_text(self) -> TaggedText | None:
        tagged_texts = self.tagged_text_repository.get_all()
        if not tagged_texts:
            return None
        return random.choice(tagged_texts)

    def make_tag_attempt(self, text_id: str, attempt: list[tuple[str, str]]) -> TagAttemptResult:
        tagged_text = self.tagged_text_repository.get(text_id)
        results = [(t1[0], t1[1] == t2[1]) for t1, t2 in zip_longest(
            tagged_text.tags, attempt, fillvalue=("", "")) if t1[0] not in string.punctuation]
        correct = sum(1 for r in results if r[1])
        score = int(100 / len(results) * correct)
        return TagAttemptResult(score, results)

    @staticmethod
    def get_original_text(tags: list[tuple[str, str]]) -> str:
        end_marker = (".", "?")
        markers = end_marker + ("'s", "'m", "'re", "n't", "'ve", ",")
        word_tag_pairs = nltk.bigrams(tags)
        result = ""
        for (a, b) in word_tag_pairs:
            if b[0] in markers:
                result += a[0]
            else:
                result += a[0] + " "
            if b[0] in end_marker:
                result += b[0]
        return result

    def add_tagged_text(self, text: str) -> TaggedText:
        tags = [nltk.tag.str2tuple(t) for t in text.split()]
        original_text = self.get_original_text(tags)
        an_id = self.id_generator.generate_id()
        tagged_text = TaggedText(an_id, original_text, tags, textstat.flesch_reading_ease(original_text))
        self.tagged_text_repository.add(tagged_text)
        return tagged_text
