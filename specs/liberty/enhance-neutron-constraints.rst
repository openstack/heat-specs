..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
 Enhance constraints for properties
===================================

https://blueprints.launchpad.net/heat/+spec/enhance-property-constraints

We need more constraints for neutron properties so that we can validate them
before stack creation.

Problem description
===================

Since we have many type of properties, some of them have custom constraints,
e.g. nova.flavor, glance.image etc. But still some of them have some certain
format as input, e.g. IP address, MAC address, network cidr, protocol etc.
It's better to check input format before passing them to CLI or stack
creation. It's helpful for users, so that they can get error message during
validation instead of stack create/update failed.

Proposed change
===============

Add custom constraints for IP address, mac address, network cidr.
For IP address constraint, it's going to be like this:

::

  constraints=[
      constraints.CustomConstraint('ip_addr')
  ]

For mac address constraint, it's going to be like this:

::

  constraints=[
      constraints.CustomConstraint('mac_addr')
  ]

For CIDR constraint, it's going to be like this:

::

  constraints=[
      constraints.CustomConstraint('net_cidr')
  ]

We can apply these constraints to neutron properties or
template parameters.


Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ethan Lynn

Milestones
----------

Target Milestone for completion:
  liberty-2

Work Items
----------

1. Add IPv4/IPv6 address format constraint

2. Add mac address format constraint

2. Add network cidr format constraint


Dependencies
============

None
