Introduction
============

`ftw.publisher.example` is a example integration package providing a
workflow integration for `ftw.publisher`. `ftw.publisher` is a staging
and publishing system for Plone contents.

This package is installed on both systems, the editor system (sender)
and the public system (receiver) - using the corresponding extras_requires.

It provides the following:

* A simple custom workflow, registered for the standard content types,
  providing the default states `private`, `pending`, `published` and
  `revision` with the corresponding transitions.

* Event handlers for the workflow transitions, wich automatically
  publishes the object on certain transitions.

* Sanity checks which are configured as conditions for the transitions.
  They check, if it's possible to publish the object (e.g. parent is
  published) and display warnings if referenced objects are not
  published.


Installing
----------

On the sender system, just add the package to your buildout using the
"sender" extras_require. You should also add a cronjob (ClockServer)
which invokes the execution of the publisher queue.

You need to create a ClockServer-user on the *sender* instance with
"Manager" role on the plone site. This username / password you need
to configure in the sender buildout. The user will then be used to
invoke the queue execution using Products.ClockServer.

sender buildout.cfg::

    [buildout]
    ...

    [instance1]
    ...
    eggs +=
        ftw.publisher.example[sender]
        Products.ClockServer
    zcml +=
        ftw.publisher.example

    zope-conf-additional =
        <clock-server>
            method /PLONESITE/@@publisher-config-executeJobs
            period 600
            user SENDER_USER_WITH_MANAGER_ROLE
            password USERS_PASSWORD
        </clock-server>


receiver buildout.cfg::

    [buildout]
    ...

    [instance1]
    ...
    eggs +=
        ftw.publisher.example[receiver]
    zcml +=
        ftw.publisher.example

Then you need to add a second user on the *receiver* instance, which
will receive the publisher jobs and create / update objects. Therefore
he has to have enough priviledges.

Once you have installed the plone-sites, go to the publisher control
panel on your *sender* instance (within the plone control panel) and add
the target plone site URL (realm) and the username / password of the
user created on the *receiver* instance.


Links
=====

The main project package is `ftw.publisher.sender` since it contains all the
configuration panels and the most tools - but without the other mandatory
packages it will not work.
Here are some additional links:

- Publisher packages on pypi: http://pypi.python.org/pypi?%3Aaction=search&term=ftw.publisher&submit=search
- Main github project repository: https://github.com/4teamwork/ftw.publisher.sender
- Issue tracker: https://github.com/4teamwork/ftw.publisher.sender/issues
- Wiki: https://github.com/4teamwork/ftw.publisher.sender/wiki
- Source code repository of the example package: https://github.com/4teamwork/ftw.publisher.example

Credits
=======

Sponsored by `4teamwork GmbH <http://www.4teamwork.ch/>`_.

Authors:

- `jone <http://github.com/jone>`_
