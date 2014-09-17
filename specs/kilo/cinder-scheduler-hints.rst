..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


==============================
Support Cinder scheduler hints
==============================

https://blueprints.launchpad.net/heat/+spec/cinder-scheduler-hints

When creating volumes with Cinder, passing scheduler hints can be necessary to
select an appropriate back-end.  This spec proposes to add a 'scheduler_hints'
option for OS::Cinder::Volume objects, as is it already done for
OS::Nova::Server.


Problem description
===================

Currently, it is not possible to pass hints to the Cinder scheduler when using
Heat to create volumes.


Proposed change
===============

Add a new optional key-value map (named 'scheduler_hints') for
OS::Cinder::Volume resources.  A user can pass hints to the Cinder scheduler by
specifying one or more keys-values in scheduler_hints.

Alternatives
------------

None


Usage Scenario
==============

For instance, request creation of `volume-A` on a different back-end than
`volume-B` using the different_host scheduler hint::

   resources:
     volume-A:
       type: OS::Cinder::Volume
       properties:
         size: 10
         scheduler_hints: {different_host: {Ref: volume-B}}


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  adrien-verge

Milestones
----------

Target Milestone for completion:
  Kilo-1

Work Items
----------

* Extend OS::Cinder::Volume to support a new 'scheduler_hints' option
* When set, pass this option to the Cinder client


Dependencies
============

* Support Cinder API version 2
  https://blueprints.launchpad.net/heat/+spec/support-cinder-api-v2
