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

============================
Implement SyncPoint DB table
============================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-graph-progress

Problem description
===================

As we traverse the dependency graph during an update, we need to keep a record
of our progress so that we can resume the traversal later in case it is
interrupted.

Proposed change
===============

Add a new table, `SyncPoint`, to the database with the following rows:

- `resource_id` (a Resource key)
- `is_update` (Boolean - True for update, False for cleanup)
- `traversal_id` (UUID)
- `stack_id` (a Stack key)
- `input_data` (JSON data)

The first three fields should form a composite primary key. That should allow
us to do a quick get of a SyncPoint given a graph key (resource key + is_update
direction) and traversal ID (i.e.  without doing a query). The stack key
together with the traversal ID allows us to query for all of the SyncPoints
associated with a particular traversal (e.g.  to delete them if the traversal
is cancelled.)

The input data will contain a map of graph keys (resource key of the Resource
that was current at the beginning of the update + is_update direction) to
resource key (may be different if the resource was replaced), RefID and
attribute data. Thus the input data pushed from previously-updated resources is
cached until such time as the current resource is ready for it. This data will
likely be serialised in JSON format, and could be quite large.

A prototype for this is
https://github.com/zaneb/heat-convergence-prototype/blob/resumable/converge/sync_point.py

Updates to the input data must be atomic, and must use the "UPDATE ... WHERE
..." form discussed in
http://www.joinfu.com/2015/01/understanding-reservations-concurrency-locking-in-nova/
- which probably means adding an extra integer field that is incremented on
every write (since we can't really query on a text field).

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

- Implement the new table and DB migration
- Implement an API for creating and updating entries

Dependencies
============

- https://blueprints.launchpad.net/heat/+spec/convergence-push-data
- https://blueprints.launchpad.net/heat/+spec/convergence-stack-data
- https://bugs.launchpad.net/heat/+bug/1415237
