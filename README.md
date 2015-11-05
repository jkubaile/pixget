# pixget
Python based pictures download script.

Download all image urls given by an input file. Each line must contain one url.

Images will be stored in a (automatically created) subdirectory with the current timestamp as name. You can also provide an output directory explicitly.

```
usage: pixget [-h] [-i INFILE] [-o OUTPUT]

Get some pix by file input.

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        Path to input file (default: input.txt)
  -o OUTPUT, --output OUTPUT
                        Output directory name (defaults to current timestamp:
                        2015-11-05-10-13, will be added if default, otherwise
                        it must exist! Existing content will be overwritten)
```

###Example content

```
http://www.zettwerk.com/logo.png
http://www.zettwerk.com/logo.png
http://www.zettwerk.com/logo.png
http://www.zettwerk.com/logo.png
http://www.zettwerk.com/unternehmen/ueber-uns/viewletImage
http://www.zettwerk.com/unternehmen/ueber-uns/viewletImage
http://www.zettwerk.com/unternehmen/ueber-uns/viewletImage
http://www.zettwerk.com/unternehmen/ueber-uns/does-not-exists
http://mywebserver.com/images/271947.jpg
invalid-url-example-will-be-igonored
http:another-one
http://mywebserver.com/images/24174.jpg

http://somewebsrv.com/img/992147.jpg
```

###Output

```

Getting 11 urls...

1: http://www.zettwerk.com/logo.png -> 2015-11-05-10-33/logo.png
2: http://www.zettwerk.com/logo.png -> 2015-11-05-10-33/logo-1.png
3: http://www.zettwerk.com/logo.png -> 2015-11-05-10-33/logo-2.png
4: http://www.zettwerk.com/logo.png -> 2015-11-05-10-33/logo-3.png
5: http://www.zettwerk.com/unternehmen/ueber-uns/viewletImage -> 2015-11-05-10-33/viewletImage.png
6: http://www.zettwerk.com/unternehmen/ueber-uns/viewletImage -> 2015-11-05-10-33/viewletImage-1.png
7: http://www.zettwerk.com/unternehmen/ueber-uns/viewletImage -> 2015-11-05-10-33/viewletImage-2.png
8: http://www.zettwerk.com/unternehmen/ueber-uns/does-not-exists -> Invalid response code: 404
9: http://mywebserver.com/images/271947.jpg -> No image found - header is: text/html
10: http://mywebserver.com/images/24174.jpg -> No image found - header is: text/html
11: http://somewebsrv.com/img/992147.jpg -> No image found - header is: text/html


The following lines were ignored, cause they are no valid urls

invalid-url-example-will-be-igonored
http:another-one
```

The image filename will be taken from the url. If there are multiple urls using the same filename, they will be appended by a counter.

###Install

As there is no egg released on pypi yet, just download/clone this repository to your local machine and use:

```
> cd /path/to/your/pixget
> /path/to/your/python setup.py install
```

to install it.