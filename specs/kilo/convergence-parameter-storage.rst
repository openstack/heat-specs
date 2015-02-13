..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..
 This template should be in ReSTructured text. The filename in the git
 repository should match the launchpad URL, for example a URL of
 https://blueprints.launchpad.net/heat/+spec/awesome-thing should be named
 awesome-thing.rst .  Please do not delete any of the sections in this
 template.  If you have nothing to say for a whole section, just write: None
 For help with syntax, see http://sphinx-doc.org/rest.html
 To test out your formatting, see http://www.tele3.cz/jbar/rest/rest.html

=====================================================
Move Parameter data storage from Stack to RawTemplate
=====================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-parameter-storage

Problem description
===================

The target state of a stack is not defined by a template alone, but by a
combination of a template and an environment (including input parameter
values). However, currently these are stored separately - there is a
RawTemplate database table for templates, but the environment is stored in the
Stack table.

In order to allow the user to roll back to a previous state, we need to store
both the old template and the old environment.

Proposed change
===============

Move the storage of the environment from the `parameters` column of the Stack
table to the RawTemplate table.  In this way, we can roll back to a previously
commanded state whenever its template is still available in the database.

While we are at it, we should add an out-of-band indicator of whether the
parameters are encrypted, since we know that encrypting the parameters in the
database is something we will want to implement.

We can also consider storing the user parameters and other parts of the
environment separately. The current design is a result of retrofitting the
environment where previously we only had parameters. We should probably store
the "files" section of the environment as a multipart-MIME document in a
separate column, rather than as a JSON dict as part of the environment, since
that is the format we want to allow in a future v2 API.

Alternatives
------------

Instead of just storing multiple references to templates in the Stack table, we
could also include multiple versions of the environment (e.g. have a
`previous_parameters` or `previous_environment` row). This would save doing the
migration now, but it would be messier and more error-prone to implement
rollback in convergence.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ckmvishnu

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Database migration
- Change how environment data is loaded from the database


Dependencies
============

None
