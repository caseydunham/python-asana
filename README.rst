Python Asana
============

.. image:: https://travis-ci.org/caseydunham/python-asana.png?branch=master
        :target: https://travis-ci.org/caseydunham/python-asana

A python wrapper around the Asana (asana.com) API

Introduction
------------

This library provides a pure python interface for the Asana restful API.

Currently not all operations are supported. All of the operations that are currently supported are read only.

With this initial version, the following functionality is working:

   * Retrieving workspaces
   * Retrieving projects
   * Retrieving users
   * Retrieving tasks
   * Retrieving stories

Documentation
-------------
Forthcoming.

Using
-----

The library provides a python wrapper around the Asana API and data model.

*Model:*

The various API methods in the pyasana.API class return instances of the following
classes

.. code-block:: pycon
   pyasana.User
   pyasana.Workspace
   pyasana.Project
   pyasana.Task
   pyasana.Story

*API:*

All interaction with the Asana API is done through the pyasana.Api class.

All Asana API calls require an Integrator Key.

To create an instance of the pyasana.Api class:

    >>> import pyasana
    >>> api = pyasana.Api("YOUR ASANA INTEGERATOR KEY")

To retrieve a list of all the workspaces:

		>>> workspaces = api.get_workspaces()
		>>> print ["%s:%s" % (w.id, w.name) for w in workspaces]
		[u'193074061952:Shiny New Workspace', u'652052755897:Sandbox']

To retrieve a list of all projects in a workspace:

		>>> workspace = 193074061952
    >>> projects = api.get_projects(workspace)
    >>> print ["%s:%s" % (p.id, p.name) for p in projects]
    [u'983421735560:Asana Python Client', u'992461725871:Test Project']

To retrieve a list of all tasks in a project:

    >>> project = 983421735560
    >>> tasks = api.get_tasks(project=project)
    >>> print ["%s:%s % (t.id, t.name) for t in tasks]
		[u'953421755459:fix task detail issue', u'953341245215:documentation']

More examples forthcoming...

.. _`the repository`: http://github.com/caseydunham/python-asana
.. _AUTHORS: https://github.com/caseydunham/python-asana/blob/master/AUTHORS.rst
