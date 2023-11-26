from abc import ABC, abstractmethod

from jinja2 import Environment, FileSystemLoader


class HtmlTemplates(ABC):
    @abstractmethod
    def render(self, name: str, context: dict) -> str:
        pass


class Jinja2Templates(HtmlTemplates):
    def __init__(self, templates_directory: str):
        self.env = Environment(loader=FileSystemLoader(templates_directory))

    def render(self, name: str, context: dict) -> str:
        t = self.env.get_template(name)
        return t.render(context)
