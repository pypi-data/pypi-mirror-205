pftag
=====

|Version| |MIT License| |ci|

Abstract
--------

This software provides a string token parser, useful in cases where a
fixed *a priori* template string is to be resolved at run time by some
process.

Overview
--------

``pftag`` is a simple app that is both a stand alone client as well as a
python module. Its main purpose is to parse *template strings*. A
template string is one where sub-parts of the string are *tokenized* by
a token marker. These tokens are resolved at execution time.

From a taxonomy perspective, ``pftag`` is an example of a string-based
(somewhat opinionated) SGMLish parser.

Installation
------------

Local python venv
~~~~~~~~~~~~~~~~~

For *on the metal* installations, ``pip`` it:

.. code:: bash

   pip install pftag

docker container
~~~~~~~~~~~~~~~~

.. code:: bash

   docker pull fnndsc/pftag

Runnning
--------

Script mode
~~~~~~~~~~~

To use ``pftag`` in script mode simply call the script with appropriate
CLI arguments

.. code:: bash


   pftag --tag "run-%timestamp-on-%platform-%arch.log"

   run-2023-03-10T13:41:58.921660-05:00-on-Linux-64bit-ELF.log

Module mode
~~~~~~~~~~~

There are several ways to use ``pftag`` in python module mode. Perhaps
the simplest is just to declare an object and instantiate with an empty
dictionary, and then call the object with the ``tag`` to process.

If additional values need to be set in the declaration, use an
appropriate dictionary. The dictionary keys are *identical* to the
script CLI keys (*sans* the leading ``--``):

.. code:: python

   from pftag import pftag

   str_tag:str = r'run-%timestamp-on-%platform-%arch.log'

   tagger:pftag.Pftag      = pftag.Pftag({})
   d_tag:dict              = tagger(str_tag)

   # The result is in the
   print(d_tag['results'])

Arguments
---------

The set of CLI arguments can also be passed in a dictionary of

.. code:: python

   {
           "CLIkey1": "value1",
           "CLIkey2": "value2",
   }

.. code:: html

          --tag <tagString>
           The tag string to process.

           [--lookupDictAdd <listOfDictionaryString>]
           A string list of additional named lookup dictionary tags and values to
           add.

           [--tagMarker <mark>]
           The marker string that identifies a tag (default "%")

           [--funcMarker <mark>]
           The marker string that pre- and post marks a function (default "_").

           [--funcArgMarker <mark>]
           The marker string between function arguments and also between arg list
           and function (default "|").

           [--funcSep <mark>]
           The marker string separating successive function/argument constructs
           (default ",").

           [--inputdir <inputdir>]
           An optional input directory specifier. Reserverd for future use.

           [--outputdir <outputdir>]
           An optional output directory specifier. Reserved for future use.

           [--man]
           If specified, show this help page and quit.

           [--verbosity <level>]
           Set the verbosity level. The app is currently chatty at level 0 and level 1
           provides even more information.

           [--debug]
           If specified, toggle internal debugging. This will break at any breakpoints
           specified with 'Env.set_trace()'

           [--debugTermsize <253,62>]
           Debugging is via telnet session. This specifies the <cols>,<rows> size of
           the terminal.

           [--debugHost <0.0.0.0>]
           Debugging is via telnet session. This specifies the host to which to connect.

           [--debugPort <7900>]
           Debugging is via telnet session. This specifies the port on which the telnet
           session is listening.

Available tags and functions
----------------------------

Adding New Tags and Lookups
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Additional tag lookup structures can be added with either the CLI or
directly using the python API, for example:

::

   # CLI
   pftag --lookupDictAdd '[{"credentials": {"user": "Jack Johnson", "password": "123456"}}]' \
         --tag "At time %timestamp, user '%user' has password '%password'."

or equivalently in python:

.. code:: python

   from pftag  import pftag

   # Declare the tag processor
   tagger:pftag.Pftag   = pftag.Pftag({})

   # Add the "credentials" lookup
   status:bool = tagger.lookupDict_add(
     [
       {"credentials":
           {
             "user":  "Jack Johnson",
             "password": "1234567"
           }
       }
     ]
   )

   str_tag:str = r"At time %timestamp, user '%user' has password '%password'."

   # and... run it!
   d_tag:dict = tagger.run(str_tag)
   if d_tag['status']: print(d_tag['result'])

both should result in something similar to:

::

   At time 2023-04-28T11:36:19.448559-04:00, user 'Jack Johnson' has password '1234567'.

For kicks, let’s hash the password to 10 chars:

::

   # CLI
   pftag --lookupDictAdd '[{"credentials": {"user": "Jack Johnson", "password": "123456"}}]' \
         --tag "At time %timestamp, user '%user' has password '%password' with password hash %password_md5|10_."

resulting in

::

   At time 2023-04-28T11:57:45.217532-04:00, user 'Jack Johnson' has password '123456' with password hash e10adc3949.

The following tags are internal/reserved:

::

               %literal   : simply replace the tag with the word 'literal'.
                            This tag is only useful in conjunction with the
                            'echo' function and together they provide a means
                            to inject arbitary text typically for md5 hashing.
               %name      : return the os.name
               %platform  : return the platform.system()
               %release   : return the platform.release()
               %machine   : return the platform.machine()
               %arch      : return the '%s' % platform.architecture()
               %timestamp : return the current timestamp

Functions
~~~~~~~~~

The lookup from any tagged string can be further processed by the
following functions

::

           md5|<chars>         : perform an md5hash on the upstream, limit result
                                 to <chars> characters

                                   eg: "%timestamp_md5|4_"

                                 replace the %timestamp in the input string with
                                 an md5 hash of 4 chars of the actual timestamp.

           chrplc|<t>|<n>      : replace <t> with <n> in the upstream input.

                                   eg: "%timestamp_chrplc|:|-_"

                                 replace the %timestamp in the input string with
                                 the actual timestamp where all ":" are replaced with
                                 "-".

           strmsk|<mask>       : for each '*' in mask pattern use ups tream char
                                 otherwise replace with <mask> char .

                                   eg: "%platform_strmsk|l****_"

                                 replace the %platform in the input string with
                                 a string that starts with an 'l' and don't change
                                 the subsequent 4 characters. If the %platform
                                 has more than 4 characters, only return the 5
                                 chars as masked.

           dcmname|<s>|<tail>  : replace any upstream %VAR with a DICOM formatted
                                 name. If <s> is passed, the seed the faker module
                                 with <s> (any string) -- this guarantees that calls
                                 with that same <s> result in the same name. If
                                 <tail> is passed, then append <tail> to the name.

                                   eg: %NAME_dcmname_

                                 may produce "BROOKS^JOHN". Each call will have
                                 a different name. However,

                                   %NAME_dcmname|foobar_

                                 will always generate "SCHWARTZ^THOMAS". While

                                   %NAME_dcmname|foobar|^ANON

                                 will generate "SCHWARTZ^THOMAS^ANON"

           echo|<something>    : Best used with the %literal tag for legibility, will
                                 replace the tag with <something>. Be careful of commas
                                 in the <something>. If they are to be preserved you
                                 will need to set --funcSep to something other than a
                                 comma.

                                   %literal_echo|why-are-we-here?_

                                 will replace the %literal with "why-are-we-here".
                                 This is most useful when literal data is to obscured
                                 in a template. For instance:

                                   %literal_echo|Subject12345,md5|5_

                                 where say "Subject12345" is privileged information but
                                 important to add to the string. In this case, we can
                                 add and then hash that literal string. In future,
                                 if we know all the privileged strings, we can easily
                                 hash and then and lookup in any `pftag` generated
                                 strings to resolve which hashes belong to which
                                 subjects.

Function detail
---------------

.. _overview-1:

Overview
~~~~~~~~

In addition to performing a lookup on a template string token, this
package can also process the lookup value in various ways. These process
functions follow a Reverse Polish Notation (RPN) schema of

::

   tag func1(args1) func2(args2) func3(args3) ...

which reading from left to right is taken as a heap from top to bottom:

::

   tag
   func1(args1)
   func2(args2)
   func3(args3)

where first the ``<tag>`` is looked up, then this lookup is processed by
``<func1>``. The result is then processed by ``<func2>``, and so on and
so forth, each functional optionally with a set a arguments. This RPN
approach also mirrors the standard UNIX piping schema.

Syntax
~~~~~~

A function (or function list) that is to be applied to a ``<tag>`` is
connected to the tag with a ``<funcMarker>`` string, usually ’\_’. The
final function should end with the same ``<funcMarker>``, so

::

   %tag_func1,func2,...,funcN_

will apply the function list in order to the tag value lookup called
“tag”; each successive evaluation consuming the result of its
predecessor as input.

Some functions can accept arguments. Arguments are passed to a function
with a ``<funcArgMarker>`` string, typically ``|``, that also separates
arguments:

::

   %tag_func|a1|a2|a3_

will pass ``a1``, ``a2``, and ``a3`` as parameters to “func”.

Finally, several functions can be chained within the ``_``\ …\ ``_`` by
separating the ``<func>|<argList>`` constructs with commas, so
pedantically

::

   %tag_func1|a1|a2|a3,func2|b1|b2|b3_

All these special characters (tag marker, function pre- and post, arg
separation, function separation) can be overriden. For instance, with a
selection of

::

   --tagMarker "@" --funcMarker "[" --funcArgMarker "," --funcSep "|"

strings can be specified as

::

   @tag[func,a1,a2,a3|func2,b1,b2,b3[

where preference/legibilty is left to the user.

Development
-----------

Instructions for developers.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To debug, the simplest mechanism is to trigger the internal remote
telnet session with the ``--debug`` CLI. Then, in the code, simply add
``Env.set_trace()`` calls where appropriate. These can remain in the
codebase (i.e. you don’t need to delete/comment them out) since they are
only *live* when a ``--debug`` flag is passed.

Testing
~~~~~~~

Run unit tests using ``pytest``.

.. code:: bash

   # In repo root dir:
   pytest

*-30-*

.. |Version| image:: https://img.shields.io/docker/v/fnndsc/pftag?sort=semver
   :target: https://hub.docker.com/r/fnndsc/pftag
.. |MIT License| image:: https://img.shields.io/github/license/fnndsc/pftag
   :target: https://github.com/FNNDSC/pftag/blob/main/LICENSE
.. |ci| image:: https://github.com/FNNDSC/pftag/actions/workflows/build.yml/badge.svg
   :target: https://github.com/FNNDSC/pftag/actions/workflows/build.yml
