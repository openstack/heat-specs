..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================
Conditional exposure of resources based on user roles
=====================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/conditional-resource-exposure

Expose resources as available based on actual user roles.

Problem description
===================

Currently we unconditionally register and present to the user all resource
plugins that we have in-tree.
As we will move in-tree some contrib/ resources that require special roles
for instantiation (e.g. Keystone resources) all users will see them
as available despite that the user might not actually be able to use them
due to RBAC restrictions.
This would be confusing to users and facilitate later stack failure
at creation instead of failing early at validation.

Proposed change
===============

Add optional settings in ``heat.conf``
(in ``[clients]`` section to be used for every client or in ``[client_*]``
section for a specific client) specifying the list of required "special"
roles to instantiate restricted resources of this service.

Use these values during validation to compare the roles with the roles from
the context to check for resource availability for the specific user who has
made the request.

Default value (empty list) of the new config option will mean
show the resource as available to any user.


Alternatives
------------

Keep the things as they are continuing to confuse users and fail later than
earlier for templates with resources that current user can not create without
having special roles.

Long term alternative / improvement would be to wait until Keystone implements
fine grained policy control and querying as part of API.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Pavlo Shchelokovskyy <pshchelo>

Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

- add config options for client plugins describing the required special
  roles list
- add an attribute to resources requiring special roles that marks them as such
- add an extra parameter to SupportStatus hinting that this resource will
  likely require a special role a common user would not generally have

  - modify docs generation to flag such resources

- add validation step comparing the options from config with roles from context
- unit tests
- functional tests

  - modify DevStack to automatically configure Heat with DevStack's default
    policies in respect to special roles for new Keystone client options
  - check if Keystone resources are listed if called from non-admin users
  - check that template containing Keystone resources is failing validation

Dependencies
============

- blueprint keystone-based-resource-availability is implemented
- admin-requiring resources are moved in-tree from contrib/
