#!/usr/bin/env python3

import ast
import mistune
import os
import pkg_resources


_type_renderers = {}

_page_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>{style}</style>
  </head>
  <body>
    {body}
  </body>
</html>
"""


def eval_block(code, globals=None):
    """Like the built-in exec(), but if the last statement is an expression,
    returns its result.
    """
    block = ast.parse(code)

    # Expr are expressions that appear as a statement by itself
    if len(block.body) > 0 and type(block.body[-1]) == ast.Expr:
        last = block.body.pop()
    else:
        last = None

    exec(compile(block, "<string>", mode="exec"), globals)
    if last:
        try:
            return eval(compile(ast.Expression(last.value), "<string>", mode="eval"), globals)
        except Exception as e:
            print(e)
            raise e


class ReportRenderer(mistune.HTMLRenderer):
    def __init__(self, type_renderers={}):
        super().__init__(True, True) # escape, allow_harmful_protocols
        self.title = ""
        self.globals = {}
        self.type_renderers = type_renderers

    def text(self, text):
        return text.format(**self.globals)

    def heading(self, text, level, **attrs):
        # remember the first h1 as title
        if level == 1 and not self.title:
            self.title = text
        return super().heading(text, level, **attrs)

    def block_code(self, code, info=None):
        if info == None or info == "python":
            v = eval_block(code, self.globals)
            return self.block_eval_result(v)
        else:
            return super().block_code(code, info)

    def block_eval_result(self, value):
        if value is None:
            return ""
        if fn := self.type_renderers.get(type(value)):
            return fn(value)
        else:
            return self.paragraph(mistune.escape(str(value)))


def render(text, style=None):
    if style is None:
        style = pkg_resources.resource_string(__package__, "style.css").decode()

    r = ReportRenderer(_type_renderers)
    md = mistune.create_markdown(renderer=r, plugins=["footnotes"])
    body = md(text)
    return _page_template.format(title=r.title, style=style, body=body)


def register(t):
    """Decorate a render function to register it for type `t`.

    Render functions take a value and return a string containing html. For
    example:

        @register(list)
        def render_b(l):
            items = '\n'.join(f"<li>{i}</li>" for i in l)
            return f"<ul>{items}</ul>"
    """
    def renderer(fn):
        _type_renderers[t] = fn
    return renderer

