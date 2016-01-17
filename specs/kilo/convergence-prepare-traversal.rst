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

============================================================
Load and generate the dependency graph for a stack traversal
============================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-prepare-traversal

Problem description
===================

We need to precalculate the graph of dependencies between all extant resources
in the stack, including versions of resources that are now out of date.

Proposed change
===============

When applying a transformation to a stack, load all extant resources for that
stack from the DB. If one or more versions of a resource in the template
already exist, select the most up-to-date one to update provided it is in a
valid state. If no versions of a resource in the template exist in the
database, create one for it.

Calculate the dependency graph, such that we will visit all of the selected
resources in dependency order to update them where neccessary and visit *all*
of the resources in reverse dependency order to clean them up where neccessary.
Clean-up operations on a resource must always happen after any update operation
on the same resource.

Finally, replace the traversal ID with a new UUID and create a SyncPoint for
each node in the graph with this traversal ID. It should also create a
SyncPoint for the stack itself, which will be used to indicate when the update
portion of the traversal is complete, at which time the stack status can be
updated.

This code should largely follow the prototype in
https://github.com/zaneb/heat-convergence-prototype/blob/resumable/converge/stack.py

If two updates are racing, one of them will fail to atomically update the Stack
row with its own newly-generated traversal ID. In this case it should roll back
the database changes, by deleting any newly-created Resource rows that it added
as well as all of the SyncPoints.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  rh-s

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Load all resources from a Stack
- Determine which resources are the most up-to-date
- Create new resources where required
- Generate the graph for traversal
- Create SyncPoints for every node in the graph
- Roll back any changes made in the database if we lose the race to be the next
  update
- Create developer documentation


Dependencies
============

- https://blueprints.launchpad.net/heat/+spec/convergence-config-option
- https://blueprints.launchpad.net/heat/+spec/convergence-graph-progress
- https://blueprints.launchpad.net/heat/+spec/convergence-stack-data
- https://blueprints.launchpad.net/heat/+spec/convergence-resource-table
