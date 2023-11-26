from abc import ABC, abstractmethod

import nltk


class LanguageService(ABC):
    @abstractmethod
    def pos_tag(self, text: str) -> list[tuple[str, str]]:
        pass


class NLTKLanguageService(LanguageService):
    def pos_tag(self, text: str) -> list[tuple[str, str]]:
        return nltk.pos_tag(nltk.word_tokenize(text))
