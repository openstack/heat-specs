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

====================================
 Support neutron subnet pool in heat
====================================

https://blueprints.launchpad.net/heat/+spec/subnet-pools

Adds resource plugin for Neutron subnet pool.

Problem description
===================

Neutron now supports `subnetpools` API extension. This helps in
managing the lifecycle of a subnet pool and using it during
subnet create/update as illustrated below.

.. code-block:: sh

    neutron subnetpool-create –default-prefixlen 24 –pool-prefix \
        10.10.0.0/16 webpool
    neutron subnet-create –subnetpool webpool websubnet

Proposed change
===============

1. Add following Resources under resources/openstack/neutron/

* OS::Neutron::SubnetPool

    * name
        Name of the subnet pool to create.
        - optional
        - type: String
        - update_allowed
    * prefixes
        A list of subnet prefixes to assign to the subnet pool.
        - required
        - type: List
        - update_allowed
        - constraints: Non empty list of CIDR
    * address_scope
        An address scope to assign to the subnet pool.
        - optional
        - type: String
        - update_allowed
        - constraints: 'neutron.address_scope' custom constraint
    * default_quota
        A per-tenant quota on the prefix space that can be allocated from the
        subnet pool for tenant subnets.
        - optional
        - type: Integer
        - update_allowed
        - constraints: Greater than or equal to 0
    * default_prefixlen
        Size of the prefix to allocate when the cidr or prefixlen attributes
        are not specified for a subnet. This would be defaulted to
        min_prefixlen if not specfied.
        - optional
        - type: Integer
        - update_allowed
        - constraints: Greater than or equal to 0
    * min_prefixlen
        Smallest prefix that can be allocated from a subnet pool.
        - optional
        - type: Integer
        - update_allowed
        - constraints: Greater than or equal to 0
    * max_prefixlen
        Maximum prefix that can be allocated from a subnet pool.
        - optional
        - type: Integer
        - update_allowed
        - constraints: Greater than or equal to 0
    * is_default
        Whether this is default IPv4/IPv6 subnet pool. There can only be
        one default subnet pool for each IP family.
        - optional
        - type: Boolean
        - update_allowed
    * tenant_id
        ID of the tenant who owns the subnet pool. Only administrative users
        can specify a tenant ID other than their own.
        - optional
        - type: String
    * shared
        Whether shared across all tenants, default is False.
        - optional
        - type: Boolean

2. Add 'subnetpool' and 'prefixlen' properties for OS::Neutron::Subnet
   resource. Also, apply a custom constraint 'neutron.subnetpool' to
   'subnetpool' property.


Alternatives
------------
None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
    ramishra@redhat.com

Milestones
----------
Target Milestone for completion:
  mitaka-2

Work Items
----------

* Add SubnetPool resource
* Add property for Subnet resource
* Add required custom constraints (neutron.address_scope, neutron.subnetpool)
* Add related tests
* Add sample template using SubnetPool in heat-templates


Dependencies
============

None
