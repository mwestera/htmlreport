from contextlib import redirect_stdout
from contextlib import contextmanager
import tempfile
import webbrowser
import io
import base64
import matplotlib.pyplot as plt
import pandas
import sys
import markdown
import builtins


@contextmanager
def htmlreport(file=None, show=False):
    """
    Makes plt.show print the plots in base64 (show=True to also display them directly), and (if
    not piped/redirected in the terminal) redirects print to a temporary html file (or a file if provided).
    Temporary file is opened in the browser.
    """

    old_pandas_str = pandas.DataFrame.__str__
    old_plt_show = plt.show
    old_print = builtins.print

    pandas.DataFrame.__str__ = pandas.DataFrame.to_html

    if not show:
        plt.show = lambda: (print(plot_to_html()), plt.close())
    else:
        plt.show = lambda: (print(plot_to_html()), old_plt_show(), plt.close())

    builtins.print = lambda *x: old_print(markdown.markdown(', '.join(y.__str__() for y in x), output_format='html'))

    if file:
        with open(file, 'w') as f:
            with redirect_stdout(f):
                yield
    elif sys.stdout.isatty:
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            with redirect_stdout(f):
                yield
            webbrowser.open('file://' + f.name)
    else:
        yield

    plt.show = old_plt_show
    pandas.DataFrame.__str__ = old_pandas_str
    builtins.print = old_print


def plot_to_html():
    """
    Turns the current matplotlib plot into a base64-encoded string embedded into an HTML <img> tag.
    This stores the images right inside the HTML. This is space-inefficient (no image compression),
    but convenient in other ways.
    https://stackoverflow.com/a/63381737
    """
    s = io.BytesIO()
    plt.savefig(s, format='png', bbox_inches="tight")
    plot_base64 = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return f'<img src="data:image/png;base64,{plot_base64}">'
