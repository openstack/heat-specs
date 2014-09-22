..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
 Convergence
=============================

https://blueprints.launchpad.net/heat/+spec/convergence

Clouds are noisy - servers fail to come up, or die when the underlying
hypervisor crashes or suffers a power failure. Heat should be resilient
and allow concurrent operations on any sized stack.

Problem description
===================

There are multiple problems that face users of Heat with the current model.

* stacks that fail during creation / update
* Physical resources may (silently) stop working - either
  disappearing or have an error of some sort (e.g. loadbalancer that
  isn't forwarding traffic, or nova instance in ERROR state). When this
  happens a subsequent update that depends on a presumably "active"
  resource is likely to fail unexpectedly.
* Heat engines are also noisy:

    * they get restarted when servers need to get updated
    * they may fail due to hardware or network failure (see under
      hypervisor failure)
    * Heat engine failures show up as a _FAILED stack, which is a
      problem for the user, but it should not be as whatever happened is a
      temporary problem for the operator, and not resolvable by the user.

* Large stacks exceed the capacity of a single heat-engine process
  to update / manage efficiently.
* Large clusters - e.g. 10K VMs should be directly usable
* Stack updates lock state until the entire thing has converged again
  which prevents admins making changes until its completed

    * This makes it hard/impossible to do autoscaling as autoscaling
      decisions may be more frequent than the completion time from
      each event

        * Concern: Why would you make a controller that makes decisions
          so frequently that it does not have time to observe the
          effects of one decision before making the next?

    * Large admin teams are forced to use an external coordination
      service to ensure they don't do expensive updates except when
      there is scheduled time
    * Reacting to emergencies is problematic

User Stories
------------

* Users should only need to intervene with a stack when there
  is no right action that Heat can take to deliver the current
  template+environment+parameters. E.g. if a cinder volume attached to a
  non-scaling-group resource goes offline, that requires administrative
  intervention -> STACK_FAILED

    * Examples that this would handle without intervention

        * nova instances that never reach ACTIVE
        * neutron ports that aren't reachable
        * Servers in a scaling group that disappear / go to ERROR in
          the nova api

    * Examples that may need intervention

        * servers that are not in a scaling group which go to ERROR
          after running for a while or just disappear
        * Scaling groups that drop below a specified minimum due to
          servers erroring/disappearing.

* Heat users can expect Heat to bring a stack into line with the
  template+parameters even if the world around it changes after
  STACK_READY - e.g. due to a server being deleted by the user.

    * That said, there will be times where users will want to disable
      this feature.

* Operators should not need to manually wait-or-prepare heat engines
  for maintenance: assume crash/shutdown/failure will happen and have
  that be seamless to the user.

    * Stacks that are being updated must not be broken / interrrupted
      in a user visible way due to a heat engine reboot/restart/redeploy.

* Users should be able to deploy stacks that scale to the size of
  the backend storage engine - e.g. we should be able to do a million
  resources in a single heat stack (somewhat arbitrary number as a
  target). This does not mean a 1 million resource single template,
  but a single stack that has 1 million resources in it, perhaps by
  way of resource groups and/or nested stacks.

* Users need to be able to tell heat their desired template+parameters
  at any time, not just when heat believes the stack is 'READY'.

    * Autoscaling is a special case of 'user' here in that it tunes
      the sizes of groups but otherwise is identical to a user.
    * Admins reacting to problematic situations may well need to make
      'overlapping' changes in rapid fire.

* Users deploying stacks with excess of 10K instances (and thus
  perhaps 50K resources) should expect Heat to deploy and update said
  stacks quicky and gracefully, given appropriate cloud capacity.

* Existing stacks should continue to function. "We don't break
  user-space".

* During stack create, the creation process is stuck waiting for a signal
  that will never come due to out of band user actions. An update is
  issued to remove the signal wait.

* During stack create, software initialization is failing because of
  inadequate amounts of space allocated in volumes. Update is issued to
  allocate larger volumes.

* During stack delete, the deletion process is waiting indefinitely to
  delete an undeletable resource. Update is issued to change the deletion
  policy and not try to remove the physical resource.

Proposed change
===============

This specification is primarily meant to drive an overall design. Most
of the work will be done under a set of sub-blueprints:

* Move from using in-process-polling to observe resource state, to an
  observe-and-notify approach. This will be the spec ``convergence-observer``.
* Move from a call-stack implementation to a continual-convergence
  implementation, triggered by change notification. This will be the spec
  ``convergence-engine``.
* Run each individual convergence step with support from the taskflow
  library via a distributed set of workers.

Prior to, and supporting, that work will be database schema changes.
The primary changes are to separate desired and observed state, and to
support the revised processing technique.  To separate desired and
observed state we will: (1) clone the table named resource, making a
table named resource_observed (the table named resource_data seems
more like part of the implementation of certain kinds of resources and
so does not need to be cloned), and (2) introduce a table named
resource_properties_observed.  For the resource_observed table, the
columns named status, status_reason, action, and rsrc_metadata will be
removed.  The raw template will be part of the desired state.  A given
resource's properties, in the desired state, are computed from the
template and effective environment (which includes the stack
parameters).  In the observed state a resource's properties are held
in the resource_properties_observed table; it will have the following
fields.

1. id VARCHAR(36)
2. stack_id VARCHAR(36)
3. resource_name VARCHAR(255)
4. prop_name VARCHAR
5. prop_value VARCHAR

Upon upgrade of the schema and engines, existing stacks will automatically
start using the convergence model.

No required changes will be made to existing API's, including the resource
plugin API.

Convergence Engine
------------------

A new set of internal RPC calls will be created to allow per-resource
convergence operations to be triggered by the observers. A new set of
public API calls will also be needed to trigger convergence on a stack
or resource manually.

There was a plan previously to only use the existing stack-update to
enable a manual convergence. This would result in a somewhat awkward
user experience that would require more of the user than is necessary.

Observer Engine
---------------

A new set of internal RPC calls will be created to trigger immediate
observation of reality by the observer. A new set of public API calls will
also be needed to trigger observation of a stack or resource manually.

Note that this will build on top of the calls introduced in
the`stack-check` blueprint by allowing a resource-check as well.

Data Model
----------

Heat will need a new concept of a `desired state` and an `observed state`
for each resource. Storage will be expected to serialize concurrent
modification of an individual resource's states, so that on the
per-resource level we can expect consistency.

Scheduling
----------

Heat stacks contain dependency graphs that users expect to be respected
during operations. Mutation of the goal state must be scheduled in the
same manner as it is now, but will be moved from a central task scheduler
to a distributed task scheduler.

On creation of a stack, for instance, the entire stack will be parsed
by the current engine. Any items in the graph that have no incomplete
parents will produce a direct message to the convergence engine queue,
which is handled by all convergence engines. The message would instruct
the worker that this resource should exist, and the worker will make
the necessary state changes to record that. Once it is recorded, a job
to converge the resource will be created.

The converge job will create an observation job. Once the reality is
observed to match desired state, the graph will be checked for children
which now have their parents all satisfied, and if any are found, the
convergence process is started for them. If we find that there are no
more children, the stack is marked as COMPLETE.

This may produce a situation where a user with larger stacks is given
an unfair amount of resources compared to a user with smaller stacks,
because the larger stack will fill up the queue before the smaller one,
leading to long queue lengths. For now, quotas and general resource
limits will have to be sufficient to prevent this situation.

Updates will work in the exact same manner. Removed items will still be
enumerated by searching for all existing resources in the new graph,
and appropriately recording the desired state as "should not exist"
for anything not in the new graph.

Rollbacks will be enabled in the same manner as they currently are,
with the old stack definition being kept around and re-applied as the
rollback operation. If concurrent updates are done, the rollback is
always to the previous stack definition that reached a COMPLETE state. [#]_

Stack deletes happen in reverse. The stack would be recorded as "should
not exist", which will inform the convergence jobs that the scheduling
direction is in reverse.  The childless nodes of the graph would be
recorded as "should not exist" and then parents with no more children
in an active state recorded as "should not exist".

This will effectively render the convergence engine a garbage collector,
as physical resources will be left unreferenced in the graph, in a state
where they can be deleted at any time. Given the potential for cost
to the user, these resources must remain visible to the user garbage
collection must be given a high priority.

Note that the state of "should not exist" does not change the meaning
of deletion policies expressed in the template.  That will still result
in a rename and basic de-referencing if there is a policy preventing
actual deletion.

.. [#] The rollback design needs further discussion as it isn't clear
       that this would be sufficient to not violate user expectations.
       We can copy the current implementation and keep a copy of the last
       known "COMPLETE" template, and roll back by asserting that if
       a user has asked for rollback. Otherwise the fact that we allow
       relatively fast updates with convergence should allow users to
       get a better rollback experience by using version control on
       templates and environment files.

Alternatives
------------

* Improve current model with better error handling and retry support.

  * Does not solve locking/concurrency problems
  * Does not solve large stack scalability problems

Implementation
==============

Assignee(s)
-----------

This work will be broken up significantly and spread between many developers.

Milestones
----------

The bulk of this work should be completed in the "K" cycle, with the
sub-blueprints landing significant amounts of change throughout Juno.

In particular, the DB schema changes to separate desired and observed
state will come first.  Once that is done we can make a major
improvement without much change in the code structure; simply by
updating the observed state as soon as each change is made we fix the
worst problem (that a partially successful stack update does not
accurately record the resulting state).  Later comes the major code
re-org.

Work Items
----------

TBD

Dependencies
============

* Blueprints

    * convergence-observer
    * convergence-engine

* Taskflow

    * Any specific needs for taskflow should be added here.
