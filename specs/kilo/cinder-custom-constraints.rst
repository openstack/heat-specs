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

===================================
 Support Cinder Custom Constraints
===================================

https://blueprints.launchpad.net/heat/+spec/cinder-custom-constraints

Support Cinder Custom Constraints, and apply them to related resources.

Problem description
===================

Many resources have property Volume/Snapshot which related with cinder
volume/snapshot, but we haven't support corresponding custom constraints.


Proposed change
===============

1. Add cinder volume custom constraint, and to apply it for resources.
2. Add cinder snapshot custom constraint, and to apply it for resources.

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

1. Add/Apply cinder volume custom constraint.
2. Add/Apply cinder snapshot custom constraint.
3. Add UT/Tempest tests for all the changes.


Dependencies
============

None