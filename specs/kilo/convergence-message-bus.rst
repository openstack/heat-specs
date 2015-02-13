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

===========================================
Internal oslo.messaging bus for convergence
===========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-message-bus

Problem description
===================

We need a message bus for the internal worker API of convergence.

Proposed change
===============

Create a new worker service within heat-engine that is dedicated to handling
internal messages to the 'worker' (a.k.a. 'converger') actor in convergence.
Messages on this bus will use the 'cast' rather than 'call' method to anycast
the message to an engine that will handle it asynchronously. We won't wait for
or expect replies from these messages.

The message types that will eventually be implemented on this bus are those
marked with the @asynchronous decorator in
https://github.com/zaneb/heat-convergence-prototype/blob/resumable/converge/converger.py

Alternatives
------------

We could have a separate heat-worker daemon, but there appears to be no point
in making life difficult for deployers as heat-engine can handle the same
tasks.

We could mix this into the same service as the existing RPC API that is called
by heat-api, but this is messy because the two have entirely different uses.
There is already precedent for running another RPC service inside heat-engine,
although we can't reuse that because it listens on a queue specific to the
engine id.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  kanagaraj-manickam

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Implement the new worker service in the engine
- Implement a client API to make it easy to send messages to the worker service


Dependencies
============

None
