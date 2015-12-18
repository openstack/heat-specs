# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import glob
import re

import docutils.core
import testscenarios
import testtools


class TestTitles(testscenarios.WithScenarios, testtools.TestCase):
    # create a set of excluded from testing directories
    exclude_dirs = {'templates', 'juno', 'kilo'}
    # get whole list of sub-directories in specs directory
    release_names = [x.split('/')[1] for x in glob.glob('specs/*/')]
    # generate a list of scenarious (1 scenario - for each release)
    scenarios = [("%s-release" % name, dict(release=name))
                 for name in set(release_names) - exclude_dirs]

    def _get_title(self, section_tree):
        section = {
            'subtitles': [],
        }
        for node in section_tree:
            if node.tagname == 'title':
                section['name'] = node.rawsource
            elif node.tagname == 'section':
                subsection = self._get_title(node)
                section['subtitles'].append(subsection['name'])
        return section

    def _get_titles(self, spec):
        titles = {}
        for node in spec:
            if node.tagname == 'section':
                # Note subsection subtitles are thrown away
                section = self._get_title(node)
                titles[section['name']] = section['subtitles']
        return titles

    def _check_titles(self, filename, expect, actual):
        missing_sections = [x for x in expect.keys() if (
            x not in actual.keys())]
        extra_sections = [x for x in actual.keys() if x not in expect.keys()]

        msgs = []
        if len(missing_sections) > 0:
            msgs.append("Missing sections: %s" % missing_sections)
        if len(extra_sections) > 0:
            msgs.append("Extra sections: %s" % extra_sections)

        for section in expect.keys():
            missing_subsections = [x for x in expect[section]
                                   if x not in actual[section]]
            # extra subsections are allowed
            if len(missing_subsections) > 0:
                msgs.append("Section '%s' is missing subsections: %s"
                            % (section, missing_subsections))

        if len(msgs) > 0:
            self.fail("While checking '%s':\n  %s"
                      % (filename, "\n  ".join(msgs)))

    def _check_lines_wrapping(self, tpl, raw):
        for i, line in enumerate(raw.split("\n")):
            if "http://" in line or "https://" in line:
                continue
            self.assertTrue(
                len(line) < 80,
                msg="%s:%d: Line limited to a maximum of 79 characters." %
                (tpl, i+1))

    def _check_no_cr(self, tpl, raw):
        matches = re.findall('\r', raw)
        self.assertEqual(
            0, len(matches),
            "Found %s literal carriage returns in file %s" %
            (len(matches), tpl))

    def _check_trailing_spaces(self, tpl, raw):
        for i, line in enumerate(raw.split("\n")):
            trailing_spaces = re.findall(" +$", line)
            self.assertEqual(
                0, len(trailing_spaces),
                "Found trailing spaces on line %s of %s" % (i+1, tpl))

    def test_check_extension(self):
        files = glob.glob("specs/%s/*" % self.release)
        for filename in files:
            self.assertTrue(filename.endswith(".rst"),
                            "spec's file must uses 'rst' extension.")

    def test_check_titles(self):
        # get titles from base template
        with open("specs/templates/%s-template.rst" % self.release) as f:
            template = f.read()
        base_spec = docutils.core.publish_doctree(template)
        expected_template_titles = self._get_titles(base_spec)

        files = glob.glob("specs/%s/*" % self.release)
        for filename in files:
            with open(filename) as f:
                data = f.read()

            spec = docutils.core.publish_doctree(data)
            titles = self._get_titles(spec)
            self._check_titles(filename, expected_template_titles, titles)

    def test_check_lines_wrapping(self):
        files = glob.glob("specs/%s/*" % self.release)
        for filename in files:
            with open(filename) as f:
                data = f.read()
            self._check_lines_wrapping(filename, data)

    def test_check_no_cr(self):
        files = glob.glob("specs/%s/*" % self.release)
        for filename in files:
            with open(filename) as f:
                data = f.read()
            self._check_no_cr(filename, data)

    def test_check_trailing_spaces(self):
        files = glob.glob("specs/%s/*" % self.release)
        for filename in files:
            with open(filename) as f:
                data = f.read()
            self._check_trailing_spaces(filename, data)
