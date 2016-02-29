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

==========================
 Mark Unhealthy Resources
==========================

https://blueprints.launchpad.net/heat/+spec/mark-unhealthy

Add an interface to allow the user to communicate information about the health
of a resource that Heat cannot determine on its own.

Problem description
===================

The only mechanism that Heat has for evaluating the health of a resource is to
compare its properties against the output of the relevant OpenStack API. (This
happens via the stack-check command in the current architecture, but will be
automatic on updates in the proposed Phase 2 of the Convergence architecture).
However, there may exist resources that the user (or application) knows are
unhealthy where Heat has no way of determining that. The obvious example is a
server which is running as far as Nova is concerned but is, in point of fact,
borked as far as the application is concerned.

Currently there is no way for an user (or application) to replace such a
resource without going performing multiple orchestration passes or renaming the
resource or both. Both are undesirable, and this leaves the user unable to take
advantage of Heat's ability to correctly replace a resource as part of a single
workflow.

Proposed change
===============

Add a PATCH handler to the Resource endpoint::

  /stacks/<stack_name>/<stack_id>/resources/<resource_id>

The PATCH method will accept a JSON body of the form::

  {
    'mark_unhealthy': <bool>,
    'resource_status_reason': <string>
  }

For legacy stacks, this call will fail if it cannot acquire the stack lock. For
Convergence (phase 1) stacks, the call will fail if it cannot acquire the
resource lock. This failure mode will be indicated by raising an
ActionInProgress exception in the engine, which manifests as a 409 Conflict
response to the ReST API request.

Upon receipt of this call, Heat will put the resource into the CHECK_FAILED
state if the 'mark_unhealthy' field is true. If the field is false, Heat will
put the resource in the CHECK_COMPLETE state if it was in the CHECK_FAILED
state; otherwise it will make no change.

Presence of any other fields or a missing 'mark_unhealthy' field will trigger
an Invalid Request error.

The status_reason field is optional. If present, the value of this field will
be used as the status_reason for the status change; otherwise an appropriate
default message will be recorded to indicate that the state change was due to
the resource being explicitly marked unhealthy.

It is assumed that should any future additional operations be added using the
PATCH verb on a resource, it will be invalid for them to occur in the same call
as this one. As such, the RPC call will have a specific mark_unhealthy_resource
call rather than a general patch_resource call.

Change the _needs_update() method of the StackResource and RemoteStack resource
types, such that the resource is replaced on update if it is in the
CHECK_FAILED state.  A user who wants to manually force replacement of a
*member* of a nested stack (as opposed to the nested stack itself) should mark
the member(s) as unhealthy rather than the stack itself.  Resources of any
other type that are in a FAILED state already will be replaced on a subsequent
stack update, regardless of the action (CHECK or otherwise), and this applies
equally to both legacy and convergence stacks.

Modify the InstanceGroup (and, by extension, Heat and AWS AutoscalingGroup)
types to give members in a FAILED state the highest priority for being removed
when scaling down or being updated in a rolling update. Currently, FAILED
resources are omitted when building a new template for the scaling group, so
any such resources would never be replaced by one of the same name. This change
will allow for continuity of naming in the case of a change that doesn't
permanently remove the resource due to scaling down.

Once bug 1508736 is fixed there should be no further need to make any change to
ResourceGroup. However, note that ResourceGroup and InstanceGroup both use the
same grouputils.get_members() function that filters out failed members, so the
modifications above may require changes to ResourceGroup to maintain the same
behaviour.

Alternatives
------------

It might appear desirable to have a single call to both mark the resource as
unhealthy and initiate a stack update with the existing template and
environment. However, it is better to keep the API calls orthogonal, as the
user may want to make other changes to the stack at the same time. It also
considerably simplifies implementation and testing.

We could add a separate healthy=False column to the database instead of
re-using CHECK_FAILED, but given that this is effectively a way of manually
providing information that is not available to stack-check, it makes sense to
re-use the same state. It also simplifies the logic in the engine, as we
already check for a FAILED state in many places, so re-using this state should
result in Heat just doing the Right Thing without having to add multiple checks
for another field.

An earlier version of this proposal suggested using a SOAP-style POST request
to a "mark_unhealthy" action endpoint, rather than a PATCH request to the
resource.  This is consistent with how many OpenStack APIs operate today, but
widely regarded as a non-ReSTful abomination. The currently `proposed
guidelines`_ of the API working group suggest a single "actions" endpoint for
POST requests of this type, where the body would be of the form::

  {
    "name": "mark_unhealthy",
    "args": {
      "unhealthy": <bool>,
      "resource_status_reason": <string>
    }
  }

However, this proposal is still controversial (and has been described, not
inaccurately, in reviews as "SOAP in ReST clothing"). The main driver behind it
seems to be a belief that projects will be unwilling to implement a fully
ReSTful interface like that proposed here.

.. _proposed guidelines: https://review.openstack.org/#/c/234994/

We could re-use the existing signal API instead of adding a new endpoint.
However, that would mean a mix of responsibility in handling signals between
the resource plugin (which is responsible today) and Heat (since this new
proposal is independent of resource type). It would be more consistent with the
currently-proposed API guidelines; it's arguable whether that is a good thing
or not, since those recommendations are still very much liable to change.

Alternatively, we could make this a call on a stack (rather than an individual
resource), so that the user can mark multiple resources unhealthy with a single
call. One downside of this is that it requires the resource identifier to be
included in the body of the request rather than the URL, so it could end up
harder than it needs to be to include in e.g. Mistral workflows. It's also less
logical from a ReST perspective, and complicates error handling and reporting.
We can always add this later if it really turns out to be required.

Instead of defining a particular state transition, we could allow the user to
set arbitrary resource states. This is a giant can of worms.

This proposal is an alternative to the one presented in
https://review.openstack.org/#/c/212205/ which involved mechanisms to place the
member IDs of various types of scaling groups under user control. This proposal
is both more generic and more relevant to the future convergence plans than
that one.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ahmed-h-elkhouly <ahmed.h.elkhouly@gmail.com>

Milestones
----------

Target Milestone for completion:
  mitaka-3

Work Items
----------

- Modify StackResource and RemoteStack such that they are replaced on update
  when in the CHECK_FAILED state.
- Implement an RPC API to mark resources as CHECK_FAILED in both the legacy and
  convergence architectures in heat-engine
- Implement a ReST front end to the RPC API call in heat-api
- Implement client support for the API call
- Modify InstanceGroup to keep FAILED resources in the template (so that they
  are replaced by another of the same name)

Dependencies
============

It is possible that the changes to InstanceGroup could be greatly simplified
after the completion of the blueprint scaling-group-common.

The replacement of failed ResourceGroup members will not work correctly in the
case of a rolling update until bug 1508736 is fixed.
