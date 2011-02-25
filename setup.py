#! /usr/bin/env python
#
# $Id: setup.py,v 1.9 2004/01/21 22:51:40 richard Exp $

from distutils.core import setup

# perform the setup action
from webunit import __version__
setup(
    name = "webunit", 
    version = __version__,
    description = 
        "Unit test your websites with code that acts like a web browser.",
    long_description = '''This release includes:

- send correct newline in mimeEncode (thanks Ivan Kurmanov)
- handle Max-Age set to 0 (thanks Matt Chisholm)

Webunit is a framework for unit testing websites:

- Browser-like page fetching including fetching the images and stylesheets
  needed for a page and following redirects
- Cookies stored and trackable (all automatically handled)
- HTTP, HTTPS, GET, POST, basic auth all handled, control over expected
  status codes, ...
- DOM parsing of pages to retrieve and analyse structure, including simple
  form re-posting
- Two-line page-fetch followed by form-submit possible, with error checking
- Ability to register error page content across multiple tests
- Uses python's standard unittest module as the underlying framework
- May also be used to regression-test sites, or ensure their ongoing
  operation once in production (testing login processes work, etc.)
''',
    author = "Richard Jones",
    author_email = "richard@mechanicalcat.net",
    url = 'http://mechanicalcat.net/tech/webunit/',
    download_url = 'http://pypi.python.org/pypi/webunit',
    packages = ['webunit', 'demo'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Monitoring',
    ],
)

# vim: set filetype=python ts=4 sw=4 et si
