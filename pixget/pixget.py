# -*- coding: utf-8 -*-

import os
from urlparse import urlparse

import validators
import requests


class PixGet(object):

    def __init__(self, infile, output):
        self.infile = infile
        self.output = output
        self.valid_lines = []
        self.invalid_lines = []
        self.filenames = {}

    def run(self):
        """ Read the infile, make the requests and show the output. """
        self._read_infile()

        print "\nGetting %s urls...\n" % (len(self.valid_lines))

        for i, line in enumerate(self.valid_lines):
            print "%d: %s -> %s" % (i + 1,
                                    line,
                                    self._make_request(line))

        if self.invalid_lines:
            print "\n"
            print "The following lines were ignored, cause they are no " \
                "valid urls\n"
            print "\n".join(self.invalid_lines)

    def _read_infile(self):
        """ Read the given infile. Strip the lines and sort them to
        valid_lines or invalid_lines. """
        with open(self.infile, 'r') as infile:
            for line in infile:
                stripped = line.strip()
                if self._is_valid(stripped):
                    self.valid_lines.append(stripped)
                else:
                    ## just silently ignore empty lines
                    if stripped:
                        self.invalid_lines.append(stripped)

    def _is_valid(self, line):
        """ A line is valid if there is some content in it and
        it looks like a url. """
        return validators.url(line) == True

    def _make_request(self, url):
        """ Make the request and check the result. """

        response = requests.get(url)
        if response.status_code not in [200]:
            return "Invalid response code: %s" % (response.status_code)

        content_type = response.headers['content-type']
        if not content_type.startswith('image'):
            return "No image found - header is: %s" % (
                response.headers['content-type']
            )

        filename = self._generate_filename(url, content_type)

        target = os.path.join(self.output, filename)
        with open(target, 'wb') as targetfile:
            targetfile.write(response.content)

        return "%s" % (target)

    def _generate_filename(self, url, content_type):
        """ Generate the local filename, based on the url. If a filename
        is given multiple times, add a counter. """
        filename = urlparse(url).path.split('/')[-1]
        ## some image urls might not have a filename suffix, so add it
        if '.' not in filename:
            filename = '%s.%s' % (filename, content_type.split('/')[-1])

        if filename in self.filenames:
            self.filenames[filename] += 1
        else:
            self.filenames.setdefault(filename, 0)

        return filename if self.filenames[filename] == 0 \
            else '%s-%s.%s' % ('.'.join(filename.split('.')[:-1]),
                               self.filenames[filename],
                               filename.split('.')[-1])
