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

===================================================
Implement Resource convergence create/update/delete
===================================================

https://blueprints.launchpad.net/heat/+spec/convergence-resource-operations

Problem description
===================

We need to modify the operations (create/update/delete) of
heat.engine.resource.Resource to work in both the convergence architecture and
the legacy architecture.

Proposed change
===============

Create a lightweight wrapper in the worker that runs the appropriate operation
using a TaskRunner. Any code that is specific to the convergence architecture
and that shouldn't be executed in the legacy architecture can hopefully also be
contained in this wrapper.

To the extent that any changes to the create/update/delete operations
themselves are benign to the legacy architecture (for example, storing the
extra data needed by convergence in the Resource table), they should be
implemented as part of the existing operations.

The prototype
https://github.com/zaneb/heat-convergence-prototype/blob/resumable/converge/resource.py
should give a good indication of the types of changes that will be neccessary.

Alternatives
------------

An alternative would be to build separate create/update/delete operations for
convergence as part of the Resource class. We could do that if it proved
necessary, but it seems preferable to keep to a single code path as much as
possible.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  unmesh-gurjar

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Make any necessary changes to the Resource.create/update/delete
- Implement TaskRunner wrapper and call it from the relevant workflow code

Dependencies
============

- https://blueprints.launchpad.net/heat/+spec/convergence-check-workflow
