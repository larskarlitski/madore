Madore - python-enhanced markdown reports
=========================================

Pronounced like the French _m'adore_.

_madore_ is meant for writing data-heavy documents. It renders a markdown file,
evaluating all code blocks as Python and replacing them with the result of
their last expression. It also passes all text through `str.format()`.

    $ madore [-o [OUTPUT]] [--style STYLE] file

## Develop

Install [pip-tools](https://pypi.org/project/pip-tools/) in a [virtual
environment](https://docs.python.org/3/library/venv.html) and run `pip-sync` to
install dependencies. Run `pip install --editable .` to get the `madore`
executable in your `$PATH`.
