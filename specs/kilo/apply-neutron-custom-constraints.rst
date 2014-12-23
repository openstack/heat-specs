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

==================================
 Apply Neutron Custom Constraints
==================================

https://blueprints.launchpad.net/heat/+spec/apply-neutron-constraints

Apply neutron port/subnet/network/router custom constraints.


Problem description
===================

1. Neutron port/subnet/router custom constraints are defined, but not to apply.
2. Neutron network custom constraint only apply to OS::Sahara::* resources,
   should apply to other related resources.

Proposed change
===============

1. Apply neutron subnet constraint.
2. Apply neutron port constraint.
3. Apply neutron router constraint.
4. Apply neutron network constraint.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  huangtianhua@huawei.com


Milestones
----------

Target Milestone for completion:
  Kilo-1

Work Items
----------

1. Apply neutron subnet constraint.
2. Apply neutron port constraint.
3. Apply neutron router constraint.
4. Apply neutron network constraint.
5. Add UT/Tempest tests for changes.


Dependencies
============

None
