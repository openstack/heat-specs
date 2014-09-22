..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================
 Convergence Observer
======================

https://blueprints.launchpad.net/heat/+spec/convergence-observer

As a step toward implementing the ``convergence`` specification, Heat
will split operations which fall into the "observing reality" category
into a separate "observer" process.

Problem description
===================

External systems hosting the physical resources of a stack will change
independent of operations in Heat. There is a need to have a way to record
and respond to these changes.

Proposed change
===============

* Observer is responsible for managing the model of reality

    * polls nova/neutron/etc using resource `check` methods.

    * conceptually polls heat stack descriptions to update internal resources

* Data model will need to store "observed state"

* REST API will need to display "observed state"

Note that no change will be necessary to the resource plugin API. Also
note that subscribing to notifications will be done in a separate
blueprint named `convergence-continuous-observer`.

Alternatives
------------

-

Implementation
==============

Assignee(s)
-----------

Work should be spread between all developers as much as possible to help
spread awareness of how things work.

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

* Modify data model to record resource state
* Modify public API to display observed state
* Create new observer RPC API calls
* Create new observer entry point
* Move "check_active" and "check" calls to use observer API

Dependencies
============

-
