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
 Support neutron QoS in heat
=============================

https://blueprints.launchpad.net/heat/+spec/support-neutron-qos

Provides support for neutron QoS feature.


Problem description
===================

https://blueprints.launchpad.net/neutron/+spec/quantum-qos-api

After the above blueprint, neutron supports an api extension for QoS,
and now provides support for attaching/detaching QoS policy to port and
network resources(with create and update).
There are two data models QoSPolicy and QoSRule, with a relationship:
QoSRule(s)->QoSPolicy -> Port/Network. For now, neutron has implemented
one rule type, QoSBandwidthLimitRule that provides bandwidth limit on
the instance egress traffic.

Administrator of a cloud may want to offer different service levels
based on the available network resources with heat, so this blueprint
will provide support for neutron resource QoS in heat, based on above
neutron resources for QoS.


Proposed change
===============

1. Add following Resources under resources/openstack/neutron/

* OS::Neutron::QoSPolicy

    Properties:

    * name:
          - type: String
          - required: True
          - description: The name of QoS policy
          - update_allowed: True
    * description:
          - type: String
          - required: False
          - description: The description of QoS policy
          - update_allowed: True
    * shared:
          - type: Boolean
          - required: False
          - description: Whether this QoS policy be shared to other tenants
          - update_allowed: True
          - default: False
    * tenant_id:
          - type: String
          - required: False
          - description: The owner tenant ID of this QoS policy
          - update_allowed: False

    Attributes:

    * rules:
          - type: List
          - description: A list of all rules for the QoS policy

* OS::Neutron::QoSBandwidthLimitRule

    Properties:

    * policy:
          - type: String
          - required: True
          - description: ID or name of the QoS policy
          - update_allowed: False
          - constraints: Custom Constrain 'neutron.qos_policy'
    * max-kbps:
          - type: Integer
          - required: True
          - description: Max bandwidth in kbps
          - update_allowed: True
          - constraints: Range(min=0)
    * max-burst-kbps:
          - type: Integer
          - required: False
          - description: Max burst bandwidth in kbps
          - update_allowed: True
          - default: 0
          - constraints: Range(min=0)


2. Add 'qos_policy' property for OS::Neutron::Port and OS::Neutron::Network
resources:

   * qos_policy:
          - type: String
          - required: False
          - description: The name or ID of QoS policy to attach
          - update_allowed: True
          - constraints: Custom Constrain 'neutron.qos_policy'


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
Target Milestone for completion:
  mitaka-2

Work Items
----------

* Add resources related
* Add property for port and network resources
* Add related tests
* Add sample templates in heat-templates project


Dependencies
============

None
