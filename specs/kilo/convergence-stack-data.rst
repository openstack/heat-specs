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

=================================================
Add extra data to the Stack table for convergence
=================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-stack-data

Problem description
===================

The convergence design requires extra data to be stored with each Stack row in
order to manage concurrent updates.

Proposed change
===============

Add the following extra fields to the Stack table:

- `prev_raw_template` (a RawTemplate key)
- `current_traversal` (a UUID that gets changed on each update)
- `current_deps` (a list of edges in the dependency graph, stored as JSON)

We also need to ensure that modifications to the Stack table are atomic with
respect to the `current_traversal` field - if a new traversal starts then any
previous traversals should stop updating the stack data. This should be
achieved using the "UPDATE ... WHERE ..." form as discussed in
http://www.joinfu.com/2015/01/understanding-reservations-concurrency-locking-in-nova/

Alternatives
------------

None

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

- Add the database migration
- Ensure that updates are atomic w.r.t. `current_traversal`


Dependencies
============

None
