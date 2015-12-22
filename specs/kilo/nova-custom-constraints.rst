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
 Optimize Nova Custom Constraints
==================================

https://blueprints.launchpad.net/heat/+spec/nova-custom-constraints

Optimize Nova Custom Constraints, add/apply nova server constraint,
and apply nova flavor constraint.

Problem description
===================

1. Many resources have property InstanceId/Server which related with nova
   server, but until now we haven't support nova server constraints.
2. Just define nova flavor custom constraint, but not to apply it.


Proposed change
===============

1. Add nova server custom constraint, and to apply it for resources.
2. Move nova keypair and flavor custom constraints to nova.py, to make sure
   all nova custom constraints defined together.
3. Apply nova flavor constraints for resources.

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

1. Add/Apply nova server custom constraint.
2. Move nova keypair and flavor custom constraints to nova.py.
3. Apply nova flavor constraints for resources
4. Add UT/Tempest tests for all the changes.


Dependencies
============

None
