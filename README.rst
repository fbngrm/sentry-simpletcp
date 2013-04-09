sentry-simpletcp
===============

An extension for Sentry that adds support for creating simple tcp connections

Install
-------

Install the package via ``pip``::

    pip install sentry-simpletcp

You can now configure simpletcp via the plugin configuration panel within your project.

Callback Receivers
------------------

Your tcp server will recive a request whenever there is a new event, with the following data
as JSON:

::

    {
        'id': '134343',
        'project': 'project-slug',
        'message': 'This is an example',
        'culprit': 'foo.bar.baz',
        'logger': 'root',
        'level': 'error'
    }