#  Copyright (c) Paul Koenig 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ==============================================================================

import re

import plotly.express as px
import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from divfusion import Report


@pytest.fixture(params=["MINIMAL_TEST", "PLOTLY_TEST", "MULTIROW_TEST", "COMPLEX_TEST"])
def report_type(request):
    return request.param


@pytest.fixture
def report(report_type):
    """
    Create a Report object for testing.
    Parameters
    ----------
    report_type: str
        pytest.fixture

    Returns
    -------
    Report: divfusion.Report
    """
    title = report_type
    match report_type:
        case "MINIMAL_TEST":
            divs = ["<div>Test Content</div>"]
            report = Report(title, divs)
        case "PLOTLY_TEST":
            divs = [px.scatter(x=[1, 2, 3], y=[1, 2, 3]).to_html(full_html=False,
                                                                 include_plotlyjs=False,
                                                                 div_id="test_px").replace("\n", "")]
            js_libs = ["https://cdn.plot.ly/plotly-2.20.0.min.js"]
            report = Report(title, divs, js_libs=js_libs)
        case "MULTIROW_TEST":
            divs = [["<div>Test Content Row 1, Full Width</div>"],
                    ["<div>Test Content Row 2, Half Width left</div>",
                     "<div>Test Content Row 2, Half Width right</div>"],
                    ["<div>Test Content Row 3, Third Width left</div>",
                     "<div>Test Content Row 3, Third Width middle</div>",
                     "<div>Test Content Row 3, Third Width right</div>"]
                    ]
            report = Report(title, divs)
        case "COMPLEX_TEST":
            divs = [["LEFT SIDEBAR",
                     [
                         ["<div>Row 1, Full Width</div>"],
                         ["<div>Row 2, Half Width left</div>",
                          "<div>Row 2, Half Width right</div>"],
                         ["<div>Row 3, Third Width left</div>",
                          "<div>Row 3, Third Width middle</div>",
                          "<div>Row 3, Third Width right</div>"]
                     ]
                     ]
                    ]
            report = Report(title, divs)
        case _:
            raise ValueError(f"Unknown test case: {report_type}")

    return report


@pytest.fixture
def expected_html(report_type):
    """
    Get the expected HTML for a given test case.
    Parameters
    ----------
    report_type : str
        pytest.fixture

    Returns
    -------
    out : str
        expected HTML string

    """
    try:
        with open(f"../resources_test/{report_type}.html") as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"Could not find expected HTML file for test case: {report_type}")


def compare_html(html1, html2):
    """
    Compare two HTML strings. Check for equality after removing all characters that are not relevant for the comparison.
    Parameters
    ----------
    html1: str
        HTML String 1
    html2: str
        HTML String 2

    Returns
    -------
    out : bool
        True if the HTML strings are equal, False otherwise.
    """
    def prep_html(s: str):
        s = re.sub(r"[^A-Za-z%+\-.,_<>/{}()\"'0-9=#|:;]", "", s)
        return s

    html1 = prep_html(html1)
    html2 = prep_html(html2)

    return html1 == html2


def test_generate_html(report, expected_html):
    """
    Test the _generate_html method of the Report class.
    Parameters
    ----------
    report : Report
        pytest.fixture
    expected_html : str
        pytest.fixture
    Returns
    -------
    None

    """
    assert compare_html(report._generate_html(), expected_html)


def test_write(report, expected_html):
    """
    Test the write method of the Report class.
    Parameters
    ----------
    report : Report
        pytest.fixture
    expected_html : str
        pytest.fixture

    Returns
    -------

    """
    test_file_path = "test.html"

    # Assert that the contents of the file match the expected HTML.
    with Patcher():
        report.write(test_file_path)
        with open(test_file_path, "r") as f:
            assert compare_html(f.read(), expected_html)
