# Make your bare-bones data exploration script output HTML reports with a single line of code  

Data exploration often begins by printing some dataframes and stats to the terminal, and showing some plots in the usual matplotlib pop-up window (plt.show()). But at some point, you may want to turn this into a more practical (and persistent) overview report.

This package lets you do that by adding only a single line of code (well, and the `import` line). The package achieves this by crudely changing `print`, `plt.show` and `pandas.__str__` to output HTML-code and then opening the resulting file in the browser.

The resulting HTML isn't particularly fancy, but it can be made (somewhat) prettier by manually inserting some print statements with headers and the like. If you use MarkDown format in your print statements (e.g., `print('# This is a header')`, this will be converted to HTML.


## Installation

```bash
pip install git+https://github.com/mwestera/htmlreport
```

This installs the package `htmlreport`, which implements a single function of the same name, which you can import:

```python
from htmlreport import htmlreport
```

## Usage

Suppose we have a function `analyze_data` that prints some strings and some pandas tables, and shows some matplotlib plots. You can then turn this into an HTML report by doing:

```python
from htmlreport import htmlreport

def analyze_data():
    # some function that prints some stuff (e.g., markdown headers), prints 
    # some pandas dataframes and calls plt.show once or several times.
    ...

with htmlreport():
    analyze_data()
```

To write to a file you can do the following (or just pipe the output of your script into a file): 

```python
with htmlreport('test.html'):
    analyze_data()
```

And to keep the usual matplotlib pop-up windows (in addition to getting the HTML report), you can do:

```python
with htmlreport(show=True):
    analyze_data()
```

## Disclaimer

This was a bit of an experiment that turned out to be useful. Existing libraries can generate more sophisticated reports, like `plotly`, `mpld3`, `ydata-profiling`, and `matplotlib`'s own `PdfPages`. My experience is that these generally require more substantial changes to your code. The current package is meant only as a minimal step up (in some respects) from the command-line.
