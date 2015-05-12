..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Enhance Manage Service with service-stack
=========================================

https://blueprints.launchpad.net/heat/+spec/heat-manage-service-stack

Retrieves IN_PROGRESS stacks being handled in the given heat-engine and
vice-versa.

Problem description
===================

In convergence mode, a given stack is being handled by one or more heat-engines
and vice-versa. Later scenario is applicable for non-convergence mode as well.
This will help operators to track the IN_PROGRESS stacks for the given
heat-engine or vice-versa. And also useful for operator during
troubleshooting issues.

Proposed change
===============

To list the stacks for the given heat-engine:

Update stack-list command filter argument with additional parameter engine-id
as follows:

``stack-list -f engine-id <engine-id>``

Here, stack-list already supports to provide filter parameters multiple times.
So, user can filter stacks for multiple engines as well.

Corresponding REST API would be:
``GET on /v1/​{tenant_id}​/stacks?filter=engine_id:<engine-id>``

Here, multiple engine-id could be provided with comma separated.

To list the heat-engines handing the given stack:

Update heat CLI with following additional parameters:
``service-list --stack-id <stack-id>``

* stack-id - to report the list of heat-engines handling the given stack.

Corresponding REST API would be:
``GET on /v1/​{tenant_id}​/services?filter=stack_id:<stack-id>``

   ``GET on /v1/<tenant-id>/services``

Here, multiple stack-id could be provided with comma separated.

NOTE: This blueprint can be extented to provide IN_PROGRESS resources in a
given heat-engine.


Alternatives
------------
None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
    Kanagaraj Manickam (kanagaraj-manickam)

Milestones
----------
Target Milestone for completion:
  liberty-1

Work Items
----------

* DB API changes:

  * Add new API 'service_get_stacks_by' with two parameters as described in the
    solution section.

* Object changes:

  * Add corresponding changes for db api changes in the Service object methods

* RPC API changes:

  * Add corresponding RPC API for the new DB API 'service_get_stacks_by'

* REST API changes:

  * Update ServiceController and StackController to handle the new REST APIs
    as defined in the solution section.

* Heat CLI

  * Updated required CLI as defined in the solution section.

* Heat-manage command:

  * Add the similar enhancement done in CLI, (this is required by admin, in
    case all heat-engines are down)

* Add required test cases

* Documentation:

  * update documentation for REST API, heat CLI and heat-manage tool
  * update CLI and API documents to mention that engine-id parameter is
    only for admin users.

Dependencies
============

None.
