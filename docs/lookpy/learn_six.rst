six包与py2/py3的兼容性
=========================

Six provides simple utilities for wrapping over differences between Python 2 and Python 3.

使用示例
++++++++


判断所用Python的版本
--------------------
::

    >>> from six import PY2, PY3
    >>> PY2
    False
    >>> PY3
    True

类型判断
--------
::

    >>> from six import class_types, integer_types, string_types, text_types, binary_types
    >>> a = 1
    >>> isinstance(a, class_types)
    False
    >>> isinstance(a, integer_types)
    True

面向对象兼容性
-------------

绑定方法的处理
::

    >>> from six import get_unbound_function, get_method_function, get_method_self, get_function_closure, get_function_code, get_function_defaults

字典处理
::

    >>> from six import iterkeys, itervalues, iteritems, iterlists, viewkeys, viewvalues, viewitems

语法兼容性
----------

::

    >>> from six import exec_, print_, raise_from, reraise, with_metaclass, add_metaclass

字符串兼容性
-----------

::

    >>> from six import b, u, unichr, int2byte, byte2int, indexbytes, iterbytes, StringIO, BytesIO, python_2_unicode_compatible


一些包和属性的重命名
------------------

::

    >>> from six.moves import html_parser, reload_module, cPickle


附
-------

一些重命名的包

Supported renames:

+------------------------------+-------------------------------------+---------------------------------------+
| Name                         | Python 2 name                       | Python 3 name                         |
+==============================+=====================================+=======================================+
| ``builtins``                 | :mod:`py2:__builtin__`              | :mod:`py3:builtins`                   |
+------------------------------+-------------------------------------+---------------------------------------+
| ``configparser``             | :mod:`py2:ConfigParser`             | :mod:`py3:configparser`               |
+------------------------------+-------------------------------------+---------------------------------------+
| ``copyreg``                  | :mod:`py2:copy_reg`                 | :mod:`py3:copyreg`                    |
+------------------------------+-------------------------------------+---------------------------------------+
| ``cPickle``                  | :mod:`py2:cPickle`                  | :mod:`py3:pickle`                     |
+------------------------------+-------------------------------------+---------------------------------------+
| ``cStringIO``                | :func:`py2:cStringIO.StringIO`      | :class:`py3:io.StringIO`              |
+------------------------------+-------------------------------------+---------------------------------------+
| ``dbm_gnu``                  | :func:`py2:gdbm`                    | :class:`py3:dbm.gnu`                  |
+------------------------------+-------------------------------------+---------------------------------------+
| ``_dummy_thread``            | :mod:`py2:dummy_thread`             | :mod:`py3:_dummy_thread`              |
+------------------------------+-------------------------------------+---------------------------------------+
| ``email_mime_base``          | :mod:`py2:email.MIMEBase`           | :mod:`py3:email.mime.base`            |
+------------------------------+-------------------------------------+---------------------------------------+
| ``email_mime_image``         | :mod:`py2:email.MIMEImage`          | :mod:`py3:email.mime.image`           |
+------------------------------+-------------------------------------+---------------------------------------+
| ``email_mime_multipart``     | :mod:`py2:email.MIMEMultipart`      | :mod:`py3:email.mime.multipart`       |
+------------------------------+-------------------------------------+---------------------------------------+
| ``email_mime_nonmultipart``  | :mod:`py2:email.MIMENonMultipart`   | :mod:`py3:email.mime.nonmultipart`    |
+------------------------------+-------------------------------------+---------------------------------------+
| ``email_mime_text``          | :mod:`py2:email.MIMEText`           | :mod:`py3:email.mime.text`            |
+------------------------------+-------------------------------------+---------------------------------------+
| ``filter``                   | :func:`py2:itertools.ifilter`       | :func:`py3:filter`                    |
+------------------------------+-------------------------------------+---------------------------------------+
| ``filterfalse``              | :func:`py2:itertools.ifilterfalse`  | :func:`py3:itertools.filterfalse`     |
+------------------------------+-------------------------------------+---------------------------------------+
| ``getcwd``                   | :func:`py2:os.getcwdu`              | :func:`py3:os.getcwd`                 |
+------------------------------+-------------------------------------+---------------------------------------+
| ``getcwdb``                  | :func:`py2:os.getcwd`               | :func:`py3:os.getcwdb`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``getoutput``                | :func:`py2:commands.getoutput`      | :func:`py3:subprocess.getoutput`      |
+------------------------------+-------------------------------------+---------------------------------------+
| ``http_cookiejar``           | :mod:`py2:cookielib`                | :mod:`py3:http.cookiejar`             |
+------------------------------+-------------------------------------+---------------------------------------+
| ``http_cookies``             | :mod:`py2:Cookie`                   | :mod:`py3:http.cookies`               |
+------------------------------+-------------------------------------+---------------------------------------+
| ``html_entities``            | :mod:`py2:htmlentitydefs`           | :mod:`py3:html.entities`              |
+------------------------------+-------------------------------------+---------------------------------------+
| ``html_parser``              | :mod:`py2:HTMLParser`               | :mod:`py3:html.parser`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``http_client``              | :mod:`py2:httplib`                  | :mod:`py3:http.client`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``BaseHTTPServer``           | :mod:`py2:BaseHTTPServer`           | :mod:`py3:http.server`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``CGIHTTPServer``            | :mod:`py2:CGIHTTPServer`            | :mod:`py3:http.server`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``SimpleHTTPServer``         | :mod:`py2:SimpleHTTPServer`         | :mod:`py3:http.server`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``input``                    | :func:`py2:raw_input`               | :func:`py3:input`                     |
+------------------------------+-------------------------------------+---------------------------------------+
| ``intern``                   | :func:`py2:intern`                  | :func:`py3:sys.intern`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``map``                      | :func:`py2:itertools.imap`          | :func:`py3:map`                       |
+------------------------------+-------------------------------------+---------------------------------------+
| ``queue``                    | :mod:`py2:Queue`                    | :mod:`py3:queue`                      |
+------------------------------+-------------------------------------+---------------------------------------+
| ``range``                    | :func:`py2:xrange`                  | :func:`py3:range`                     |
+------------------------------+-------------------------------------+---------------------------------------+
| ``reduce``                   | :func:`py2:reduce`                  | :func:`py3:functools.reduce`          |
+------------------------------+-------------------------------------+---------------------------------------+
| ``reload_module``            | :func:`py2:reload`                  | :func:`py3:imp.reload`,               |
|                              |                                     | :func:`py3:importlib.reload`          |
|                              |                                     | on Python 3.4+                        |
+------------------------------+-------------------------------------+---------------------------------------+
| ``reprlib``                  | :mod:`py2:repr`                     | :mod:`py3:reprlib`                    |
+------------------------------+-------------------------------------+---------------------------------------+
| ``shlex_quote``              | :mod:`py2:pipes.quote`              | :mod:`py3:shlex.quote`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``socketserver``             | :mod:`py2:SocketServer`             | :mod:`py3:socketserver`               |
+------------------------------+-------------------------------------+---------------------------------------+
| ``_thread``                  | :mod:`py2:thread`                   | :mod:`py3:_thread`                    |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter``                  | :mod:`py2:Tkinter`                  | :mod:`py3:tkinter`                    |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_dialog``           | :mod:`py2:Dialog`                   | :mod:`py3:tkinter.dialog`             |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_filedialog``       | :mod:`py2:FileDialog`               | :mod:`py3:tkinter.FileDialog`         |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_scrolledtext``     | :mod:`py2:ScrolledText`             | :mod:`py3:tkinter.scrolledtext`       |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_simpledialog``     | :mod:`py2:SimpleDialog`             | :mod:`py3:tkinter.simpledialog`       |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_ttk``              | :mod:`py2:ttk`                      | :mod:`py3:tkinter.ttk`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_tix``              | :mod:`py2:Tix`                      | :mod:`py3:tkinter.tix`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_constants``        | :mod:`py2:Tkconstants`              | :mod:`py3:tkinter.constants`          |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_dnd``              | :mod:`py2:Tkdnd`                    | :mod:`py3:tkinter.dnd`                |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_colorchooser``     | :mod:`py2:tkColorChooser`           | :mod:`py3:tkinter.colorchooser`       |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_commondialog``     | :mod:`py2:tkCommonDialog`           | :mod:`py3:tkinter.commondialog`       |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_tkfiledialog``     | :mod:`py2:tkFileDialog`             | :mod:`py3:tkinter.filedialog`         |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_font``             | :mod:`py2:tkFont`                   | :mod:`py3:tkinter.font`               |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_messagebox``       | :mod:`py2:tkMessageBox`             | :mod:`py3:tkinter.messagebox`         |
+------------------------------+-------------------------------------+---------------------------------------+
| ``tkinter_tksimpledialog``   | :mod:`py2:tkSimpleDialog`           | :mod:`py3:tkinter.simpledialog`       |
+------------------------------+-------------------------------------+---------------------------------------+
| ``urllib.parse``             | See :mod:`six.moves.urllib.parse`   | :mod:`py3:urllib.parse`               |
+------------------------------+-------------------------------------+---------------------------------------+
| ``urllib.error``             | See :mod:`six.moves.urllib.error`   | :mod:`py3:urllib.error`               |
+------------------------------+-------------------------------------+---------------------------------------+
| ``urllib.request``           | See :mod:`six.moves.urllib.request` | :mod:`py3:urllib.request`             |
+------------------------------+-------------------------------------+---------------------------------------+
| ``urllib.response``          | See :mod:`six.moves.urllib.response`| :mod:`py3:urllib.response`            |
+------------------------------+-------------------------------------+---------------------------------------+
| ``urllib.robotparser``       | :mod:`py2:robotparser`              | :mod:`py3:urllib.robotparser`         |
+------------------------------+-------------------------------------+---------------------------------------+
| ``urllib_robotparser``       | :mod:`py2:robotparser`              | :mod:`py3:urllib.robotparser`         |
+------------------------------+-------------------------------------+---------------------------------------+
| ``UserDict``                 | :class:`py2:UserDict.UserDict`      | :class:`py3:collections.UserDict`     |
+------------------------------+-------------------------------------+---------------------------------------+
| ``UserList``                 | :class:`py2:UserList.UserList`      | :class:`py3:collections.UserList`     |
+------------------------------+-------------------------------------+---------------------------------------+
| ``UserString``               | :class:`py2:UserString.UserString`  | :class:`py3:collections.UserString`   |
+------------------------------+-------------------------------------+---------------------------------------+
| ``winreg``                   | :mod:`py2:_winreg`                  | :mod:`py3:winreg`                     |
+------------------------------+-------------------------------------+---------------------------------------+
| ``xmlrpc_client``            | :mod:`py2:xmlrpclib`                | :mod:`py3:xmlrpc.client`              |
+------------------------------+-------------------------------------+---------------------------------------+
| ``xmlrpc_server``            | :mod:`py2:SimpleXMLRPCServer`       | :mod:`py3:xmlrpc.server`              |
+------------------------------+-------------------------------------+---------------------------------------+
| ``xrange``                   | :func:`py2:xrange`                  | :func:`py3:range`                     |
+------------------------------+-------------------------------------+---------------------------------------+
| ``zip``                      | :func:`py2:itertools.izip`          | :func:`py3:zip`                       |
+------------------------------+-------------------------------------+---------------------------------------+
| ``zip_longest``              | :func:`py2:itertools.izip_longest`  | :func:`py3:itertools.zip_longest`     |
+------------------------------+-------------------------------------+---------------------------------------+

urllib parse
<<<<<<<<<<<<

.. module:: six.moves.urllib.parse
   :synopsis: Stuff from :mod:`py2:urlparse` and :mod:`py2:urllib` in Python 2 and :mod:`py3:urllib.parse` in Python 3

Contains functions from Python 3's :mod:`py3:urllib.parse` and Python 2's:

:mod:`py2:urlparse`:

* :func:`py2:urlparse.ParseResult`
* :func:`py2:urlparse.SplitResult`
* :func:`py2:urlparse.urlparse`
* :func:`py2:urlparse.urlunparse`
* :func:`py2:urlparse.parse_qs`
* :func:`py2:urlparse.parse_qsl`
* :func:`py2:urlparse.urljoin`
* :func:`py2:urlparse.urldefrag`
* :func:`py2:urlparse.urlsplit`
* :func:`py2:urlparse.urlunsplit`
* :func:`py2:urlparse.splitquery`
* :func:`py2:urlparse.uses_fragment`
* :func:`py2:urlparse.uses_netloc`
* :func:`py2:urlparse.uses_params`
* :func:`py2:urlparse.uses_query`
* :func:`py2:urlparse.uses_relative`

and :mod:`py2:urllib`:

* :func:`py2:urllib.quote`
* :func:`py2:urllib.quote_plus`
* :func:`py2:urllib.splittag`
* :func:`py2:urllib.splituser`
* :func:`py2:urllib.splitvalue`
* :func:`py2:urllib.unquote` (also exposed as :func:`py3:urllib.parse.unquote_to_bytes`)
* :func:`py2:urllib.unquote_plus`
* :func:`py2:urllib.urlencode`


urllib error
<<<<<<<<<<<<

.. module:: six.moves.urllib.error
   :synopsis: Stuff from :mod:`py2:urllib` and :mod:`py2:urllib2` in Python 2 and :mod:`py3:urllib.error` in Python 3

Contains exceptions from Python 3's :mod:`py3:urllib.error` and Python 2's:

:mod:`py2:urllib`:

* :exc:`py2:urllib.ContentTooShortError`

and :mod:`py2:urllib2`:

* :exc:`py2:urllib2.URLError`
* :exc:`py2:urllib2.HTTPError`


urllib request
<<<<<<<<<<<<<<

.. module:: six.moves.urllib.request
   :synopsis: Stuff from :mod:`py2:urllib` and :mod:`py2:urllib2` in Python 2 and :mod:`py3:urllib.request` in Python 3

Contains items from Python 3's :mod:`py3:urllib.request` and Python 2's:

:mod:`py2:urllib`:

* :func:`py2:urllib.pathname2url`
* :func:`py2:urllib.url2pathname`
* :func:`py2:urllib.getproxies`
* :func:`py2:urllib.urlretrieve`
* :func:`py2:urllib.urlcleanup`
* :class:`py2:urllib.URLopener`
* :class:`py2:urllib.FancyURLopener`
* :func:`py2:urllib.proxy_bypass`

and :mod:`py2:urllib2`:

* :func:`py2:urllib2.urlopen`
* :func:`py2:urllib2.install_opener`
* :func:`py2:urllib2.build_opener`
* :func:`py2:urllib2.parse_http_list`
* :func:`py2:urllib2.parse_keqv_list`
* :class:`py2:urllib2.Request`
* :class:`py2:urllib2.OpenerDirector`
* :class:`py2:urllib2.HTTPDefaultErrorHandler`
* :class:`py2:urllib2.HTTPRedirectHandler`
* :class:`py2:urllib2.HTTPCookieProcessor`
* :class:`py2:urllib2.ProxyHandler`
* :class:`py2:urllib2.BaseHandler`
* :class:`py2:urllib2.HTTPPasswordMgr`
* :class:`py2:urllib2.HTTPPasswordMgrWithDefaultRealm`
* :class:`py2:urllib2.AbstractBasicAuthHandler`
* :class:`py2:urllib2.HTTPBasicAuthHandler`
* :class:`py2:urllib2.ProxyBasicAuthHandler`
* :class:`py2:urllib2.AbstractDigestAuthHandler`
* :class:`py2:urllib2.HTTPDigestAuthHandler`
* :class:`py2:urllib2.ProxyDigestAuthHandler`
* :class:`py2:urllib2.HTTPHandler`
* :class:`py2:urllib2.HTTPSHandler`
* :class:`py2:urllib2.FileHandler`
* :class:`py2:urllib2.FTPHandler`
* :class:`py2:urllib2.CacheFTPHandler`
* :class:`py2:urllib2.UnknownHandler`
* :class:`py2:urllib2.HTTPErrorProcessor`


urllib response
<<<<<<<<<<<<<<<

.. module:: six.moves.urllib.response
   :synopsis: Stuff from :mod:`py2:urllib` in Python 2 and :mod:`py3:urllib.response` in Python 3

Contains classes from Python 3's :mod:`py3:urllib.response` and Python 2's:

:mod:`py2:urllib`:

* :class:`py2:urllib.addbase`
* :class:`py2:urllib.addclosehook`
* :class:`py2:urllib.addinfo`
* :class:`py2:urllib.addinfourl`