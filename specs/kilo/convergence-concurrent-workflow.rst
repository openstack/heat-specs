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

======================================================
Convergence workflow for dealing with locked resources
======================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-concurrent-workflow

Problem description
===================

When doing convergence with legacy resource plugins (which is all plugins in
Phase 1 of convergence), we may encounter a resource that is locked for
processing a previous update. We want to wait for this previous update to
complete and retrigger another update with the latest template.

Proposed change
===============

If the workflow encounters a resource that is locked by another engine, it
should first check that the other engine is still alive, and if not then break
the lock. Assuming the other engine is still working, the workflow should
neither process that resource nor trigger processing any subsequent nodes. To
ensure that processing of that graph node is retriggered once the previous
update is complete, we must check at the conclusion of every update whether the
traversal we are processing is still current.

Since SyncPoints belonging to previous traversals are deleted before beginning
a new one, failing to find a SyncPoint in the database is sufficient to alert
us of a potentially-waiting new traversal. If this occurs, reload the stack to
determine the current traversal, and check the SyncPoint for the current node
to determine if it is ready. If it is, then retrigger the current node with the
appropriate data for the latest traversal (which can be found in the Stack
table).

There is a race that could cause multiple triggers on the same graph node,
however it will be resolved by the lock on the resource, since only the process
that successfully acquires the lock will continue.

An exception to all of this is the case where the graph node is of the update
type and the resource status is DELETE_IN_PROGRESS. In that case, we should
simply create a replacement resource.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ananta

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Bail out when we encounter a locked resource
- Retrigger when required if a SyncPoint is not found
- Replace a resource that is still needed but has the status DELETE_IN_PROGRESS
- Create developer documentation

Dependencies
============

- https://blueprints.launchpad.net/heat/+spec/convergence-check-workflow
- https://blueprints.launchpad.net/heat/+spec/convergence-resource-locking
- https://blueprints.launchpad.net/heat/+spec/convergence-graph-progress
- https://blueprints.launchpad.net/heat/+spec/convergence-stack-data
- https://blueprints.launchpad.net/heat/+spec/convergence-resource-replacement
