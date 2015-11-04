..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

====================
Immutable Parameters
====================

https://blueprints.launchpad.net/heat/+spec/immutable-parameters

Template authors should be able to mark template parameters as
updatable or non-updatable to restrict updating parameters which have
destructive effects on the application.

Problem description
===================

Sometimes a template parameter is only intended to be passed during
stack creation.  For example, updating an SSH public key name
parameter, which is passed to the keypair property of an
OS::Nova::Server, would result in the server being replaced and risk
downtime.

In some cases, an application's architecture would not be tolerant of
certain servers being rebuilt.  The template author has the freedom to
mark parameters which cause those servers to be rebuilt as immutable.

This feature is targeted to Heat service providers and operators of
other services that offer a curated set of templates to end-users.
These are users who may not have a lot of expertise with the
application architecture.  Expert users have the option of editing the
template to remove the update restriction.

Proposed change
===============

Add a new "updatable" boolean field to the parameters section in a HOT
template.  A value of False would result in the engine rejecting
stack-updates that include changes to that parameter.  When not
specified in the template, "updatable" would default to True to ensure
backwards compatibility with old templates.

Alternatives
------------

- Loosen the "each parameter can be in one parameter group"
  restriction and use parameter groups to mark parameters as
  immutable.  Adding a new updatable field is a more user-friendly
  option.

Implementation
==============

This would include changes to heat/engine/hot/parameters.py, where a
new updatable field would be added, and heat/engine/parameters.py,
where we would restrict updates to parameters.  Whenever a user
attempts to update a restricted parameter, they will see a
ImmutableParameterModified exception returned from the API before the
actual stack-update begins.

Assignee(s)
-----------

Primary assignee:
  jasondunsmore

Milestones
----------

Target Milestone for completion:
  mitaka-2

Work Items
----------

- Add updatable field to template (heat/engine/hot/parameters.py)

- Restrict updates to parameters (heat/engine/parameters.py)

- Add a ParameterUpdateNotAllowed exception (heat/common/exception.py)

- Add unit tests

Dependencies
============

None
