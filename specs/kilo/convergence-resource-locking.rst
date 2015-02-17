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

=================================
Enable locking of Resources in DB
=================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-resource-locking

Problem description
===================

Currently we enforce locking at the stack level, so only one operation can be
in progress at a time on a stack. This is not fine-grained enough, as it
prevents us from starting a new update while awaiting the result of a previous
one. Phase one of convergence is to remove this restriction by locking at the
level of individual resources.

Proposed change
===============

Make rows in the Resource table lockable, by ensuring that state changes are
atomic. We'll also need to store the ID of the engine that currently holds the
lock, so that we can use this to detect when an engine has died and clean up
appropriately.

We'll use the "UPDATE ... WHERE ..." form discussed in
http://www.joinfu.com/2015/01/understanding-reservations-concurrency-locking-in-nova/
to ensure atomic updates.

Alternatives
------------

The existing StackLock code does almost exactly what we want already, but the
downside is that it uses a separate table in the database to do so. Using that
rather than applying new semantics to the writes we are already doing would
make convergence even more database-intensive than it already is.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ishant-tyagi

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Database migration to add the id of the engine holding the lock
- Modify the way changes to the Resource table are written to guarantee
  atomicity


Dependencies
============

None
