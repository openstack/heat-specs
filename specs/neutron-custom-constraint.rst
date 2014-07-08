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

==============================================
 Implement More Custom Constraints for Neutron
==============================================

https://blueprints.launchpad.net/heat/+spec/neutron-custom-constraint

Now only network constraint is supported for neutron, we need more constraints
like subnet, port, router etc.

Problem description
===================

Many resources have some properties related with network, now neutron custom
constraints only support network constraint, haven't support subnet/port/router
constraints.

Proposed change
===============

Add 3 custom constraints to neutron.

1. 'neutron.subnet' for subnet constraint.
2. 'neutron.port' for port constraint.
3. 'neutron.router' for router constraint.

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
  Juno-2

Work Items
----------

1. Implement subnet constraint for neutron
2. Implement port constraint for neutron
3. Implement router constraint for neutron



Dependencies
============

https://blueprints.launchpad.net/heat/+spec/glance-parameter-constraint
