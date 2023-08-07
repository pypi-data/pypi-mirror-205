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

class Report:
    """
    This is the main class for divfusion.
    It takes a List of Lists of HTML div's and writes them to disk.
    The placement of the div's is traditional C-Style, with columns being added horizontally and rows vertically.
    """

    def __init__(self, title, divs, css_files=None, js_files=None, js_libs=None):
        """
        Initialize the Report object.
        :param title: The title of the report
        :param divs: A List of Lists of HTML div's
        :param css_files: The CSS file to use
        :param js_files: The JS file to use
        :param js_libs: A List of JS libraries to use
        """
        # INPUT DEFAULTS
        if js_libs is None:
            js_libs = []
        if js_files is None:
            js_files = []
        if css_files is None:
            css_files = []

        # INPUT VALIDATION
        assert isinstance(title, str), "title must be a string!"
        assert isinstance(divs, list), "divs must be a List of Lists of strings"
        assert isinstance(css_files, list), "css_files must be a List of strings"
        assert isinstance(js_files, list), "js_files must be a List of strings"
        assert isinstance(js_libs, list), "js_libs must be a List of strings"

        self.title = title
        self.divs = divs
        self.css_files = css_files
        self.js_files = js_files
        self.js_libs = js_libs

        self.divs = self.format_divs(self.divs)

    @staticmethod
    def format_divs(divs: list):
        """
        Format the divs to be used in the report.
        :param divs: A List of Lists of HTML div's
        :return: A List of Lists of HTML div's
        """

        def format_div(_div: str):
            """
            Format the div to be used in the report.
            :param _div: An HTML div
            :return: An HTML div
            """
            if not isinstance(_div, str):
                raise TypeError("divs must be a List of Lists of strings")

            return _div

        results = []
        for div in divs:
            if isinstance(div, list):
                results.append(Report.format_divs(div))
            elif isinstance(div, str):
                results.append(format_div(div))
            else:
                raise TypeError("Divs can only contain strings!")
        return results

    def write(self, output_filepath):
        """
        Write the report to disk.
        """
        html = self._generate_html()
        with open(output_filepath, 'w+') as f:
            f.write(html)

    def _generate_html(self):
        """
        Generate the HTML for the report.
        :return: The HTML for the report
        """

        def add_divs(divs, new_container):
            """
            Adds divs recursively to a string and then return this string.
            :param new_container:
            :param divs:
            :return:
            """
            divs_string = ''
            if new_container:
                divs_string += '<div class="container text-center">\n'
            for element in divs:
                if new_container:
                    divs_string += '<div class="row">\n'
                else:
                    divs_string += f'<div class="col-md-{int(12 / len(divs))}">\n'
                if isinstance(element, list):
                    divs_string += add_divs(element, new_container=(not new_container))
                else:  # element is a string
                    divs_string += f"{element}\n"
                divs_string += '</div>\n'
            if new_container:
                divs_string += '</div>\n'

            return divs_string

        html = '<html>\n'
        html += '<head>\n'
        html += '<title>{}</title>\n'.format(self.title)
        html += '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" ' \
                'rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" ' \
                'crossorigin="anonymous">\n'
        html += '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" ' \
                'integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" ' \
                'crossorigin="anonymous"></script>\n'
        for css_file in self.css_files:
            html += '<link rel="stylesheet" href="{}">\n'.format(css_file)
        for js_lib in self.js_libs:
            html += '<script src="{}"></script>\n'.format(js_lib)
        for js_file in self.js_files:
            html += '<script src="{}"></script>\n'.format(js_file)
        html += '</head>\n'
        html += '<body>\n'
        html += add_divs(self.divs, True)
        html += '</body>\n'
        html += '</html>\n'
        return html
