..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
Add DISABLED SupportStatus
===========================

https://blueprints.launchpad.net/heat/+spec/hidden-supportstatus-improvements

The deprecation process should include a way to keep users from
creating new stacks with a resource.

Problem description
===================

When a resource is marked HIDDEN as the final step in the deprecation
process, users can still create stacks with that resource.  This could
result in an ever-growing number of stacks with the unsupported
resource.  Since removing a resource entirely will break live stacks
that contain that resource, it would be difficult to ever remove the
resource.  Even if the resource is unsupported, some level of
maintenance would be necessary to ensure the resource continues to
load.

Proposed change
===============

Modify the HIDDEN SupportStatus to disallow creation of stacks that
contain HIDDEN resources.  This will result in fewer stacks with the
unsupported resource over time, making complete removal of the
resource a future possibility.

Alternatives
------------

Leave HIDDEN as-is and create a new DISABLED status with the proposed
behavior.

Implementation
==============

Some investigation is needed, but it may be possible to pass a
parameter that indicates a create is being done as a result of an
UpdateReplace exception.  When the flag is encountered for HIDDEN
resources, the create will be allowed.  It will be disallowed for new
resource creates, during stack-create and stack-update (ie. adding a
new resource to an existing stack).

Assignee(s)
-----------

Primary assignee:
  jasondunsmore

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

- Pass a parameter during when create is called as a result of
  UpdateReplace.  These types of creates will be allowed for HIDDEN
  resources.

- Disallow stack-creates with stacks containing HIDDEN resources.

- Disallow stack-updates with stacks containing *new* HIDDEN resources.

- Add unit tests.

Dependencies
============

None
