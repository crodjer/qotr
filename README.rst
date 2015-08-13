====
QOTR
====

  Go off-the record, quickly.

.. image:: https://api.travis-ci.org/crodjer/qotr.svg
   :target: https://travis-ci.org/crodjer/qotr
.. image:: https://coveralls.io/repos/crodjer/qotr/badge.svg?branch=master
   :target: https://coveralls.io/r/crodjer/qotr?branch=master

About
=====

QOTR is a application through which you can quickly spawn a encrypted chat with
your friends. The messages are encrypted before they leave your browser. The
QOTR servers cannot understand what is being said.

For chats 256 bit AES-CES encryption is used. The key generation happens in the
browser. To keep it easy to share a chat room, the password is provided as a location hash. Browsers do not send a location hash to the server.

Try it out at the `demo server  <https://qotr.herokuapp.com/>`_.

*QOTR is a alpha quality software, not vetted by cryptography experts. Please use it carefully. Avoid sending sensitive data over this.*

How it works
------------

A fairly detailed description of how the encryption works is available `here <https://github.com/crodjer/qotr/blob/master/FLOW.rst#how-qotr-works>`_.

Why?
----

Using OTR with current common chat clients is difficult. It cannot be trivially
done over common platforms. All encrypted chat services require you to install a
new client or a plugin. This may be a turn-off for a friend who isn't concerned
about privacy and encryption. QOTR's goal is to make it convenient (as simple as
opening a URL) for them to use.


Development
===========

QOTR is a combination of a server and a browser based client. Both of them need
to be built separately.

QOTR Server
-----------

The server is based on `tornado <http://tornadoweb.org/>`_ web framework. As of
now, the channels are stored in memory, hence QOTR can only have a single
server for a endpoint.

Running/Development
```````````````````

To launch a development server:

.. code ::

    $ pip install -r requirements.txt
    $ python -m qotr.server


Tests
`````

Run tests via:

.. code ::

    $ QOTR_ENV=test nosetests --with-coverage --cover-package=qotr

QOTR Client (Ember.js)
----------------------

Prerequisites
`````````````

You will need the following things properly installed on your computer:

 - `Git <http://git-scm.com/>`_
 - `Node.js <http://nodejs.org/>`_ (with NPM)
 - `Bower <http://bower.io/>`_
 - `Ember CLI <http://www.ember-cli.com/>`_
 - `PhantoJS <http://phantomjs.org/>`_

Installation
````````````

.. code ::

    $ npm install
    $ bower install

Running / Development
`````````````````````

.. code ::

    $ ember server

Visit your app at [http://localhost:4200](http://localhost:4200). The QOTR
development server should be running locally.

Running Tests
`````````````

There are some tests in the frontend, but the coverage is not good. This is partially due to difficulty in testing a few things and partially my inexperience with ``ember-cli`` based testing.

The tests require you to have a development QOTR server running locally.

.. code ::

    $ python -m qotr.server

Execute the tests:

.. code ::

    $ ember test
    $ ember test --server

Building
````````

.. code ::

    $ ember build # development build
    $ ember build --environment production # production build

Hosting
=======

QOTR hosting has been tested on heroku (free SSL!). Add the git remote provided
in your heroku application to your local clone:

.. code ::

    $ git remote add heroku https://git.heroku.com/qotr.git

It requires multiple build packs. First, the ember application needs to be built
and then the sever requires a python based buildpack to run tornado. To enable
those, run:

.. code ::

    $ heroku buildpacks:add https://github.com/tonycoco/heroku-buildpack-ember-cli.git
    $ heroku buildpacks:add https://github.com/heroku/heroku-buildpack-python.git

Set the QOTR environment variable:

.. code ::

    $ heroku config:set QOTR_ENV=production

Deploy:

.. code ::

    $ git push heroku master


Bugs
====

Probably lots. Please send us reports on the Github `issue tracker <https://github.com/crodjer/qotr/issues>`_. Patches are welcome too.

.. _forge: https://github.com/digitalbazaar/forge
