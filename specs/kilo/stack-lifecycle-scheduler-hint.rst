..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
 Stack lifecycle scheduler hint blueprint
=========================================

https://blueprints.launchpad.net/heat/+spec/stack-lifecycle-scheduler-hint

A heat provider may have a need for custom code to examine stack requests
prior to performing the operations to create or update a stack. After the
custom code completes, the provider may want to provide hints to the nova
scheduler with stack related identifiers, for processing by any custom
scheduler plug-ins configured for nova.

Problem description
===================

A heat provider may have a need for custom code to examine stack
requests prior to performing the operations to create or update a stack.
An example would be a holistic scheduler that schedules a stack's member
compute resources as group. This would be done using a custom plugin
invoked through the stack lifecycle plugpoint. After the custom code
completes, when the create or update is being processed, any custom
schedulers configured for nova would need to map nova create requests
back to any decisions made during the call to the custom stack
lifecycle plugin. Current heat includes no identifiers in a nova
create request that can be used to map back to a Server or Instance
resource within a heat stack.

It is out of scope for this spec, but worth noting that cinder scheduler
hints are now supported by heat and may need similar treatment. See
https://review.openstack.org/#/c/126282/ and
https://review.openstack.org/#/c/126298/


Proposed change
===============

When heat processes a stack, and the feature is enabled,
the stack id, root stack id, stack resource id,
stack resource name and the path in the stack (as a list of tuples,
(stackresourcename, stackname)) will be passed to nova by heat as
scheduler hints, to the configured schedulers for nova.

The behavior changes will be optional, default disabled, and controlled
through a new heat config variable.

These five scheduler hints will be added to server creates done using
either resource class Server (OS::Nova::Server) or resource class
Instance (AWS::EC2::Instance). heat_root_stack_id will be set to the
id of the root stack of the resource, heat_stack_id will be
set to the id of the resource's parent stack,
heat_stack_name will be set to the id of the resource's
parent stack, heat_path_in_stack will be set to a list of
tuples, (stackresourcename, stackname) with list[0] being
(None, rootstackname), and heat_resource_name will be set to
the resource's name


Alternatives
------------

No reasonable alternatives were identified.
Similar function could be achieved if the lifecycle plugin modified the stack
(and changes were persisted). This would be bad behavior. It would conflict
with convergence when it lands, and scheduler decisions would become visible
to the heat user (unless somehow redacted on query).


Implementation
==============

Assignee(s)
-----------

A patch comprising a full implementation of the blueprint
(https://review.openstack.org/#/c/96889/) is already being
reviewed, under the old pre-spec process.

Primary assignee:
  William C. Arnold (barnold-8)

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

Implementation: https://review.openstack.org/#/c/96889/
Documentation: Add good documentation to heat in tree docs


Dependencies
============

No dependencies
