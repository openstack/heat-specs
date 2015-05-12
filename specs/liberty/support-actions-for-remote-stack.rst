..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


==================================
 Support actions for remote stack
==================================

https://blueprints.launchpad.net/heat/+spec/support-actions-for-remote-stack

This Blueprint will support actions such as snapshot, restore, check,
cancel-update, abandon and so on for OS::Heat::Stack resource.


Problem description
===================

We support to manager OpenStack resources across multiple regions
after the Blueprint
https://blueprints.launchpad.net/heat/+spec/multi-region-support

But now we don't support some actions such as snapshot/restore
for remote stacks.


Proposed change
===============

The changes will support some actions such as snapshot, restore, check,
cancel-update, abandon and so on for remote stack(OS::Heat::Stack resource).

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
  Liberty-1

Work Items
----------

* Support snapshot and restore for remote stacks.
* Support cancel-update for remote stacks.
* Support check for remote stacks.
* Support abandon for remote stacks.
* Add related tests for changes.

Dependencies
============

None
