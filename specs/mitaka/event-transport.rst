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

=======================
Pushing events to users
=======================

https://blueprints.launchpad.net/heat/+spec/event-transport

Problem description
===================

Currently events are stored in the database and users need to use the API to
poll them and be notified of stack changes. This particularly painful for
hooks, where Heat is waiting for user input.

Proposed change
===============

To let the user customize how he wants to get event, we add a key to the
environment to specify where they should go::

  event_sinks:
    - type: zaqar-queue
      target: myqueue
      ttl: 30

``event_sinks`` is a list of target with a type specified, and possible options
(like ``ttl`` here being a Zaqar option). Zaqar will be the first
implementation available, sending all the events to the specified queue.

We'll use an entry points with stevedore to allow pluggable implementations.

To not add network calls to the critical path of every single event, the
publication will be delegated to a thread and thus be asynchronous. The
drawback is that potential errors won't be presented to users.

Events will continue to go in the database.


Alternatives
------------

Instead of making it a user configurable option, we could make it a global
option for the Heat administrator. It makes it less discoverable, and is
probably not necessary for every users. We also lose configurability.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  therve

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

- Change the environment to handle the new element.
- Modify environment handling the client.
- Implement sending over zaqar.


Dependencies
============

- Event message format: https://review.openstack.org/231382
