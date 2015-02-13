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

==========================================
Add convergence data to the Resource table
==========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-resource-table

Problem description
===================

The convergence design requires extra data to be stored with each Resource row
in the database, in order to allow different versions of a resource to co-exist
within the same stack.

Proposed change
===============

Add the following extra fields to the Resource table:

- `needed_by` (a list of Resource keys)
- `requires` (a list of Resource keys)
- `replaces` (a single Resource key, Null by default)
- `replaced_by` (a single Resource key, Null by default)
- `current_template` (a single RawTemplate key)

(Note, the first two fields are currently known as `requirers` and
`requirements`, respectively, in
https://github.com/zaneb/heat-convergence-prototype/blob/resumable/converge/resource.py
- but those are too confusing. Once we settle on names, we should update the
simulator code as well.)

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  skraynev

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Database migration

Dependencies
============

We need to resolve https://bugs.launchpad.net/heat/+bug/1415237 first as that
will determine what the type of a Resource key is.
