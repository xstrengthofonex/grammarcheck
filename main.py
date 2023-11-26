import os
import string

from falcon import App, Request, Response, HTTPFound
from waitress import serve

from config import TEMPLATES_DIR, ROOT_DIR
from grammarcheck.html_templates import HtmlTemplates, Jinja2Templates
from grammarcheck.pos import PosFacade


class PosResource:
    def __init__(self, html_templates: HtmlTemplates, pos_facade: PosFacade):
        self.html_templates = html_templates
        self.pos_facade = pos_facade

    def on_get(self, req: Request, res: Response):
        res.status = "200 OK"
        res.content_type = "text/html"
        res.text = self.html_templates.render("pos.html", {})


class TagAttemptResource:
    def __init__(self, html_templates: HtmlTemplates, pos_facade: PosFacade):
        self.html_templates = html_templates
        self.pos_facade = pos_facade

    def on_get(self, req: Request, res: Response):
        tagged_text = self.pos_facade.get_random_tagged_text()
        res.status = "200 OK"
        res.content_type = "text/html"
        options = set([t[1] for t in tagged_text.tags if t[1] not in string.punctuation]) if tagged_text else set()
        context = {"text": tagged_text, "options": options, "punctuation": string.punctuation}
        res.text = self.html_templates.render("tag_attempt.html", context)


class TagResultResource:
    def __init__(self, html_templates: HtmlTemplates, pos_facade: PosFacade):
        self.html_templates = html_templates
        self.pos_facade = pos_facade

    def on_post(self, req: Request, res: Response, tag_id: str):
        data = req.get_media()
        tag_attempt = [(t[0].split("_")[1], t[1]) for t in data.items()]
        result = self.pos_facade.make_tag_attempt(tag_id, tag_attempt)
        context = {"result": result}
        res.status = "200 OK"
        res.content_type = "text/html"
        res.text = self.html_templates.render("tag_result.html", context)


def load_sentences(path: str, pos_facade: PosFacade):
    with open(path) as f:
        for sent in f.readlines():
            print(pos_facade.add_tagged_text(sent))


class IndexResource:
    def on_get(self, req: Request, res: Response):
        raise HTTPFound("/pos")


def create_routes(app: App):
    pos_facade = PosFacade()
    load_sentences(os.path.join(ROOT_DIR, "tagged_sentences.txt"), pos_facade)
    html_templates = Jinja2Templates(TEMPLATES_DIR)
    index_resource = IndexResource()
    pos_resource = PosResource(html_templates, pos_facade)
    tag_attempt_resource = TagAttemptResource(html_templates, pos_facade)
    tag_result_resource = TagResultResource(html_templates, pos_facade)

    app.add_route("/", index_resource)
    app.add_route("/pos", pos_resource)
    app.add_route("/pos/attempt", tag_attempt_resource)
    app.add_route("/pos/attempt/{tag_id}", tag_result_resource)


def create_app() -> App:
    app = App()
    create_routes(app)
    return app


def main():
    app = create_app()
    print("Serving at http://localhost:8000")
    serve(app, host="localhost", port=8000)


if __name__ == '__main__':
    main()
