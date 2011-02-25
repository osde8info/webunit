Web unit testing  (the concise help)
====================================

To run the current demo tests, use::

   ./run_tests demo


Installation
------------

Install the webunit libraries with::

   python setup.py install

Then make a directory like the demo one in your application with tests in
it, and invoke with::

   ./run_tests <test>

<test>
   Run the test named - just like unittest.py.


Configuration
-------------

We've found it useful to be able to test different servers with the same test
suite. To this end, we've got a simple configuration file setup. See the doc
string in webunit.config


Errors
------
If a request fails with an incorrect response code (the default valid
response codes are 200, 301 and 302) then the result body fetched from the
server will be appended to the logfile for that server.


Making requests - the WebTestCase class
---------------------------------------
The WebTestCase is best thought of as a web browser with some added features.
To truly emulate a web browser (single-threaded at present) use the "page"
methods below. For more fine-grained control and testing, use the other
methods.

The WebTestCase objects have a number of attributes (see `Setting up fetch
defaults`_):

1. protocol, server, port -- these default to http://localhost:80 and are used
   when a relative fetch is performed. Most tests set these vars up with
   setServer in the setUp method and then use relative URLs.
2. authinfo -- basic authentication information. Use setBasicAuth to set and
   clearBasicAuth to clear.
3. cookies -- the test's store of cookies
4. images -- cache of images fetched

There are two modes of retrieval using two HTTP methods:

**fetch** mode
 This is the default mode, and just fetches the HTML of a page.
**page** mode
 This is a more browser-like mode. It follows redirections and loads
 images and stylesheets required to render the page.
**GET** method
 This is the default HTTP method used.
**POST** method
 All GET methods have a HTTP POST analog, usually just with ``post``
 prefixed.

Now the actual calls that are possible:

assertCode(self, url, code=None, \*\*kw)
  Perform a HTTP GET and assert that the return code from the
  server one of the indicated codes.

get = assertCode(self, url, code=None, \*\*kw)
  Just an alias

assertContent(self, url, content, code=None, \*\*kw)
  Perform a HTTP GET and assert that the data returned from the
  server contains the indicated content string.
assertNotContent(self, url, content, code=None, \*\*kw)
  Perform a HTTP GET and assert that the data returned from the
  server contains the indicated content string.

getAssertCode = assertCode(self, url, code=None, \*\*kw)
  Just an alias

getAssertContent = assertContent(self, url, content, code=None, \*\*kw)
  Just an alias

getAssertNotContent = assertNotContent(self, url, content, code=None, \*\*kw)
  Just an alias

page(self, url, code=None, \*\*kw)
  Perform a HTTP GET using the specified URL and then retrieve all
  image and linked stylesheet components for the resulting HTML page.

post(self, url, params, code=None, \*\*kw)
  Perform a HTTP POST using the specified URL and form parameters.

postAssertCode(self, url, params, code=None, \*\*kw)
  Perform a HTTP POST and assert that the return code from the
  server is one of the indicated codes.

postAssertContent(self, url, params, content, code=None, \*\*kw)
  Perform a HTTP POST and assert that the data returned from the
  server contains the indicated content string.

postAssertNotContent(self, url, params, content, code=None, \*\*kw)
  Perform a HTTP POST and assert that the data returned from the
  server doesn't contain the indicated content string.

postPage(self, url, params, code=None, \*\*kw)
  Perform a HTTP POST using the specified URL and form parameters
  and then retrieve all image and linked stylesheet components for the
  resulting HTML page.

All of these methods eventually call fetch() - the additional \*\*kw are
passed directly to the fetch method:

fetch(self, url, postdata=None, server=None, port=None, protocol=None, ok_codes=None)
      Run a single test request to the indicated url. Use the POST data
      if supplied. If the URL is a fully-qualified one (ie. has a server
      and protocol) then that overrides the session's default, but may
      be further overridden by the method arguments.
      Raises failureException if the returned data contains any of the
      strings indicated to be Error Content.
      Returns a HTTPReponse object wrapping the response from the server.

HTTP Response objects
---------------------

The HTTPResponse objects hold all the infomation about the server's response
to the request. This information includes:

1. protocol, server, port, url - the request server and URL
2. code, message, headers - the information returned by httplib.HTTP.getreply()
3. body - the response body returned by httplib.HTTP.getfile()

Additionally, the object has several methods:

getDOM(self)
  Get a DOM for this page. See the SimpleDOM_ instructions for details

extractForm(self, path=[], include_submit=0, include_button=0)
  Extract a form (as a dictionary) from this page.
  
  The "path" is a list of 2-tuples ``('element name', index)`` to follow
  to find the form. So::

   <html><head>..</head><body>
    <p><form>...</form></p>
    <p><form>...</form></p>
   </body></html>
  
  To extract the second form, any of these could be used::

   [('html',0), ('body',0), ('p',1), ('form',0)]
   [('form',1)]
   [('p',1)]


HTTPResponse objects are also able to fetch using WebTestCase methods. They
define additional methods:

getForm(self, formnum, getmethod, postargs, \*args)
  Given this page, extract the "formnum"th form from it, fill the
  form with the "postargs" and post back to the server using the
  "getmethod" with additional "args".
    
  NOTE: the form submission will include any "default" values from
  the form extracted from this page. To "remove" a value from the
  form, just pass a value None for the elementn and it will be
  removed from the form submission.
    
  example WebTestCase::

      page = self.get('/foo')
      page.postForm(0, self.post, {'name': 'blahblah',
              'password': 'foo'})
    
  or the slightly more complex::

      page = self.get('/foo')
      page.postForm(0, self.postAssertContent, {'name': 'blahblah',
              'password': None}, 'password incorrect')


postForm(self, formnum, postmethod, postargs, \*args)
  As with getForm, only use a POST request.


Setting up fetch defaults
-------------------------

setServer(self, server, port)
  Set the server and port number to perform the HTTP requests to.

setBasicAuth(self, username, password)
  Set the Basic authentication information to the given username
  and password.

clearBasicAuth(self)
  Clear the current Basic authentication information

setAcceptCookies(self, accept=1)
  Indicate whether to accept cookies or not

clearCookies(self)
  Clear all currently received cookies


Auto-fail error content
-----------------------
You may have the fetcher automatically fail when receiving certain content
using:

registerErrorContent(self, content)
  Register the given string as content that should be considered a
  test failure (even though the response code is 200).

removeErrorContent(self, content)
  Remove the given string from the error content list.

clearErrorContent(self)
  Clear the current list of error content strings.



Cookies
-------
To test for cookies being sent _to_ a server, use:

registerExpectedCookie(self, cookie)
  Register a cookie name that we expect to send to the server.

removeExpectedCookie(self, cookie)
  Remove the given cookie from the list of cookies we expect to
  send to the server.

To test for cookies sent _from_ the server, access the cookies attribute of
the test harness. It is a dict of::

  cookies[host name][path][cookie name] = string


SimpleDOM
---------
Simple usage::

 >>> import SimpleDOM
 >>> parser = SimpleDOM.SimpleDOMParser()
 >>> parser.parseString("""<html><head><title>My Document</title></head>
 ... <body>
 ...  <p>This is a paragraph!!!</p>
 ...  <p>This is another para!!</p>
 ... </body>
 ... </html>""")
 >>> dom = parser.getDOM()
 >>> dom.getByName('p')
 [<SimpleDOMNode "p" {} (1 elements)>, <SimpleDOMNode "p" {} (1 elements)>]
 >>> dom.getByName('p')[0][0]
 'This is a paragraph!!!'
 >>> dom.getByName('title')[0][0]
 'My Document'


Form extraction example (see also the tests in the test/ directory of the
source)::

        # fetch the start page
        page = self.get('/ekit/home')
        page = page.postForm(1, self.postAssertCode, {'__ac_name': 'joebloggs',
            '__ac_password': 'foo'}, [302])
        # same as last fetch, but automatically follow the redirect
        page = page.postForm(1, self.page, {'__ac_name': 'joebloggs',
            '__ac_password': 'foo'})


Thanks
======

Thanks to everyone who's helped with this package, including supplying
hints, bug reports and (more importantly :) patches:

Gary Capell

Note that this list is nowhere near complete, as I've only just started
maintaining it. If you're miffed that you're not on it, just let me know!

