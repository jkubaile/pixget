import unittest
import tempfile
import os
import shutil

import requests_mock

from pixget.pixget import PixGet


class TestPixGet(unittest.TestCase):

    def setUp(self):
        """ some test data, a temp dir and the pixget object """
        self.good_ct = 'images/jpg'
        self.bad_ct = 'text/html'
        self.good_url = 'http://somewhere.com/image.jpg'
        self.bad_url = 'http:somewhere.com/image.jpg'
        self.tmpdir = tempfile.mkdtemp()
        self.pixget = PixGet('input.txt', self.tmpdir)

    def tearDown(self):
        """ remove temp dir """
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)

    def _setUp_infile(self, lines):
        """ helper method to create a text file with some urls in tmp
        dir. """
        infile_path = os.path.join(self.tmpdir, 'input.txt')
        with open(infile_path, 'w') as infile:
            infile.write('\n'.join(lines))
        return infile_path

    def test_make_request_404(self):
        with requests_mock.mock() as m:
            m.get(self.good_url,
                  headers={'content-type': 'image/jpeg'},
                  status_code=404)
            target = self.pixget._make_request(self.good_url)
            self.assertTrue(target.startswith('Invalid response code'))

    def test_make_request_wrong_ct(self):
        with requests_mock.mock() as m:
            m.get(self.good_url,
                  headers={'content-type': 'text/html'})
            target = self.pixget._make_request(self.good_url)
            self.assertTrue(target.startswith('No image found'))

    def test_make_request(self):
        with requests_mock.mock() as m:
            m.get(self.good_url, headers={'content-type': 'image/jpeg'})
            target = self.pixget._make_request(self.good_url)
            output_location = os.path.join(self.tmpdir, 'image.jpg')
            self.assertEquals(target, output_location)
            self.assertTrue(os.path.exists(output_location))

    def test_generate_filename_primitive(self):
        generated_same = self.pixget._generate_filename(
            self.good_url, self.good_ct
        )
        self.assertEquals(generated_same, 'image.jpg')

    def test_generate_filename_without_suffix(self):
        generated_without_dot = self.pixget._generate_filename(
            'http://somewhere.com/anotherimage', self.good_ct
        )
        self.assertEquals(generated_without_dot, 'anotherimage.jpg')

    def test_generate_filename_double_dots(self):
        generated_with_two_dots = self.pixget._generate_filename(
          'http://somewhere.com/file.name.jpg', self.good_ct
        )
        self.assertEquals(generated_with_two_dots, 'file.name.jpg')

    def test_generate_filename_counting(self):
        first = self.pixget._generate_filename(
            self.good_url, self.good_ct
          )
        self.assertEquals(first, 'image.jpg')

        ## calling again should a the counter
        second = self.pixget._generate_filename(
            self.good_url, self.good_ct
          )
        self.assertEquals(second, 'image-1.jpg')

        ## and so on...
        third = self.pixget._generate_filename(
            self.good_url, self.good_ct
          )
        self.assertEquals(third, 'image-2.jpg')

    def test_read_infile(self):
        ## one good, one bad
        infile = self._setUp_infile([self.good_url,
                                     self.bad_url])
        self.pixget = PixGet(infile, self.tmpdir)
        self.pixget._read_infile()
        self.assertEquals(len(self.pixget.valid_lines), 1)
        self.assertEquals(len(self.pixget.invalid_lines), 1)

        ## two good
        infile = self._setUp_infile([self.good_url,
                                     self.good_url])
        self.pixget = PixGet(infile, self.tmpdir)
        self.pixget._read_infile()
        self.assertEquals(len(self.pixget.valid_lines), 2)
        self.assertEquals(len(self.pixget.invalid_lines), 0)

        ## two bad
        infile = self._setUp_infile([self.bad_url,
                                     self.bad_url])
        self.pixget = PixGet(infile, self.tmpdir)
        self.pixget._read_infile()
        self.assertEquals(len(self.pixget.valid_lines), 0)
        self.assertEquals(len(self.pixget.invalid_lines), 2)

    def test_read_infile_empty_lines(self):
        infile = self._setUp_infile(['', ''])
        self.pixget = PixGet(infile, self.tmpdir)
        self.pixget._read_infile()
        self.assertEquals(len(self.pixget.valid_lines), 0)
        self.assertEquals(len(self.pixget.invalid_lines), 0)

    def test_read_infile_with_whitespaces(self):
        infile = self._setUp_infile([' %s    ' % (self.good_url)])
        self.pixget = PixGet(infile, self.tmpdir)
        self.pixget._read_infile()
        self.assertEquals(len(self.pixget.valid_lines), 1)
        self.assertEquals(len(self.pixget.invalid_lines), 0)

if __name__ == '__main__':
    unittest.main()
