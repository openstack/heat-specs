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

==============================================
Support Role-based Access Control for Networks
==============================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/support-rbac-for-networks

Currently there is no support about Role-based Access Control for Networks
in heat. So add a new namespace called OS::Neutron::RBACPolicy for the rbac
resource.

Problem description
===================

There are new rbac-policies api in Liberty which needed to be supported
by heat. We need to add a new namespace for it.


Proposed change
===============

we need to add the following resource

RBACPolicy

Specification.
--------------

RBACPolicy
----------

Create a RBAC policy for a given tenant.

Namespace:
OS::Neutron::RBACPolicy

Required Properties:
--------------------
object_type:
  Type of the object that RBAC policy affects.
  String Value.

target_tenant:
  ID of the tenant to which the RBAC policy will be enforced.
  String Value.
  Update allowed.

action:
  Action for the RBAC policy.
  String Value.

object_id:
  ID or name of the RBAC object.
  String Value.

Supported object_type and action:
---------------------------------
SUPPORTED_TYPES_ACTIONS = {'network': ['access_as_shared']}


Optional Properties:
--------------------
tenant_id:
  The owner tenant ID. Only required if the caller has an administrative
  role and wants to create a rbac for another tenant.
  String Value.


References
----------

https://blueprints.launchpad.net/neutron/+spec/rbac-networks

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Di XiaoLi <dixiaobj@cn.ibm.com>


Milestones
----------

Target Milestone for completion:
  mitaka-3

Work Items
----------

* Add new namespace for OS::Neutron::RBACPolicy resource.

Dependencies
============

None
