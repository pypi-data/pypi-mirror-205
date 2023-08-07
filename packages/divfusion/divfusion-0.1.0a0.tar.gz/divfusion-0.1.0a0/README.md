# divfusion

`divfusion` is a Python class that generates an HTML-Report from a set of HTML divs. In practise, these divs would
originate from other Python modules, especially those that generate plots (e.g. `matplotlib`, `seaborn`, `plotly`).

If used with plotly, this closes between a single-figure plotly export and a full-fledged plotly-dash server, which
needs to be hosted somewhere. Using this Library, all interactivity of plotly is preserved (hovering, zooming, buttons,
dropdowns, etc.). In addition to that, you can add html-exports of your pd.DataFrames, images or any other HTML content.
`divfusion` brings all of this together and manges the layout and style of the report for you (bring your own css is
possible).

The resulting html file is completely self-contained and can be opened in any browser on any device.

## Installation

You can install `divfusion` via pip:

```bash
pip install divfusion
```

## Usage

To use `divfusion.Report`, you must first import the class:

```python
from divfusion import Report
```

Next, create a new instance of `Report` by passing the following parameters:

* `title` - The title of the report (string)
* `divs` - A list of HTML divs, can be nested (list)
* `css_files` (optional) - The CSS files to include (list)
* `js_files` (optional) - The JS files to include (list)
* `js_libs` (optional) - A list of JS libraries to include (list)

```python
report = Report(title="My Report",
                divs=[["<h1>Heading 1</h1>", "<p>Paragraph 1</p>"], ["<h2>Heading 2</h2>", "<p>Paragraph 2</p>"]])
```

To generate the HTML report, call the `write` method and pass the file path where you want to save the report:

```python
report.write("path/to/report.html")
```

## Example

Here's an example of how to use `divfusion.Report`:

```python
from divfusion import Report

report = Report(title="My Report",
                divs=[["<h1>Heading 1</h1>", "<p>Paragraph 1</p>"],
                      ["<h2>Heading 2</h2>", "<p>Paragraph 2</p>"]])
report.write("path/to/report.html")
```

This will generate an HTML report with the title "My Report" and two rows of HTML divs. The first row contains a heading
and a paragraph, and the second row contains a subheading and another paragraph. The report will be saved to the file
path specified.

## Dependencies

Currently `divfusion` does not require any dependencies.

## Future Work

- Add support for custom css
- Provide easy-to-use wrapper functions for adding plotly-figures, pandas-dataframes, etc.

## Contribution

I welcome any and all contributions, no matter what size. Please feel free to open an issue or pull request.

## License

Apache License 2.0