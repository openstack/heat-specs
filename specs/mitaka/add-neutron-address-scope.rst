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

=============================
Support Neutron Address Scope
=============================

https://blueprints.launchpad.net/heat/+spec/add-neutron-address-scope

Provides support for Neutron address scope feature.

Problem description
===================

Address scope feature in Neutron has been available since
Liberty release:

https://blueprints.launchpad.net/neutron/+spec/address-scopes


An address scope can be associated with multiple subnet pools
in a one-to-many relationship. The subnet pools under an address
scope must not overlap.

This blueprint will add the neutron address scope resource in heat.

Proposed change
===============

Add following resource under resources/openstack/neutron/

* OS::Neutron::AddressScope

    * name (required, name of the address scope, update_allowed)
    * tenant_id (optional, the owner tenant ID of the address scope)
      - limited to administrator operate
      - apply 'keystone.project' constraint

    * shared (optional, indicating whether the address scope is shared,
      default value is False, update_allowed)
      - limited to administrator operate, can change unshared to shared only

    * ip_version (optional, default value is 4)
      - allowed values are [4, 6]


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

  mitaka-2

Work Items
----------

* Add resource related
* Add related tests
* Add sample template in heat-templates

Dependencies
============

None
