..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
Add support for SR-IOV-PORT
====================================

https://blueprints.launchpad.net/heat/+spec/neutron-resource-add-pci-port

When creating Neutron SR-IOV ports, these ports should have their own resource
types. This spec proposes to add vnic_type to OS::Neutron::Port objects.

Problem description
===================

A neutron port is a virtual port that is either attached to a linux bridge or
an openvswitch bridge on a compute node. With the introduction of PCI
Passthrough SR-IOV support, the intermediate virtual bridge is no longer
required. Instead, the SR-IOV port is associated with a virtual function
that is supported by the vNIC adaptor.

Currently a PCI port can be created by setting the value_specs property
in OS::Neutron::Port. However, having a new resource type will simplify
the templates for the user and allow for different constraints in the
future.


Proposed change
===============

Add support for vnic_type OS::Neutron::Port.
Provider resources will be used to create a PCI resource.
OS::Neutron::Port will be modified to suport the vnic type.

The properties for OS::Neutron::Port will be as follows:

.. code-block:: yaml

  resources:
    sriov_port:
      type: OS::Neutron::Port
      properties:
        network: { get_param: my_net }
        vnic_type: direct


The vnics type supported are normal, direct and macvtap


Alternatives
------------

Implement a new resource OS::Neutron::PciPort. This will reside with the
current Neutron::Port and reuse as much of Neutron::Port as possible.

The properties for OS::Neutron::PciPort will be as follows:

.. code-block:: yaml

  resources:
    sriov_port:
      type: OS::Neutron::PciPort
      properties:
        network: { get_param: my_net }
        vnic_type: direct


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Rob Pothier


Milestones
----------

Target Milestone for completion:
  Kilo-1

Work Items
----------

* modify OS::Neutron::Port https://review.openstack.org/#/c/129353/

Dependencies
============

None
