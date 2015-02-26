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

=====================================
Port tests from convergence simulator
=====================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-simulator-tests

Problem description
===================

In coming up with the design of convergence, we built a simulator that verifies
a substantial number of test scenarios. The scenarios are defined in what
amounts to a simple DSL. If we can run the exact same scenarios against the
real Heat code base, then we can not only verify that our convergence
implementation fullfills the requirements of the simulator but also continue to
do that over time, even as we add more scenarios and even if we still have the
need to rapidly prototype design changes in the simulator.

Proposed change
===============

Implement a stub for the RPC APIs that puts messages into in-memory queues that
are drained by an event loop.

Implement a fake resource type that uses an in-memory store to represent the
underlying physical resource.

Provide wrappers for the global inputs to the scenario - `reality`, `verify`,
`Template`, `RsrcDef`, `GetRes`, `GetAtt`, `engine`, `converger` - that allow
them to be backed by the real equivalent classes in Heat.

Finally, reimplement
https://github.com/zaneb/heat-convergence-prototype/blob/resumable/test_converge.py
using testtools primitives and passing the wrappers above as globals, rather
than those defined in
https://github.com/zaneb/heat-convergence-prototype/blob/resumable/converge/__init__.py#L24-L41

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

- Implement RPC stub and event loop
- Implement fake TestResource type and backend simulator
- Implement wrappers to map the scenario DSL to real Heat classes
- Implement a unit test framework to run the scenarios

Dependencies
============

- https://blueprints.launchpad.net/heat/+spec/convergence-message-bus

Of course, few of these tests are going to pass until Phase 1 of convergence is
substantially complete.
