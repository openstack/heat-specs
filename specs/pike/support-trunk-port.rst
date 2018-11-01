..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Support Neutron Trunk resource
==============================

https://blueprints.launchpad.net/heat/+spec/support-trunk-port/

Add Heat support for Neutron trunk resource.

Problem description
===================

Neutron introduced a new resource called `trunk`_ in the Newton release. This
resource makes possible to connect a VM to multiple Neutron networks using a
single port called trunk parent port.

A typical workflow for using a trunk is the following:

* Prepare the used networks and ports:

.. code-block:: sh

  openstack network create net0
  openstack network create net1
  openstack network create net2
  openstack port create --network net0 port0
  openstack port create --network net1 port1
  openstack port create --network net2 port2

* Create a trunk and set ``port0`` as a parent port:

.. code-block:: sh

  openstack network trunk create --parent-port port0 trunk0

* Add ``port1`` and ``port2`` to the trunk and set segmentation type and ID:

.. code-block:: sh

  openstack network trunk set \
      --subport port=port1,segmentation-type=vlan,segmentation-id=101 trunk0
  openstack network trunk set \
      --subport port=port2,segmentation-type=vlan,segmentation-id=102 trunk0

* Launch a VM by adding the parent port (``port0``) only.

* The VM can access to ``net0`` using untagged traffic, ``net1`` using VLAN ID
  ``101``, and ``net2`` using VLAN ID ``102``.

This Blueprint proposes a change to support Neutron trunks in Heat by
introducing a new Heat resource: OS::Neutron::Trunk

.. _trunk: https://blueprints.launchpad.net/neutron/+spec/vlan-aware-vms

Proposed change
===============

Implement a new ``OS::Neutron::Trunk`` resource under
``engine/resources/openstack/neutron/`` with the following properties and
attributes:

Properties:

* name:
    - description: The name of the trunk
    - required: True
    - type: String
    - update_allowed: True
* parent_port:
    - description: ID or Name of the parent port
    - required: True
    - type: String
    - update_allowed: False
    - constraints: 'neutron.port'
* subports:
    - description: List with 0 or more map elements containing subport details
    - required: False
    - update_allowed: True
    - type: list; List contents: Map value expected

  Map properties:

    - port:
        + description: ID or name of a port to be used as a subport
        + required: True
        + update_allowed: True
        + type: String
        + constraints: 'neutron.port'
    - segmentation_type:
        + description: may be required by certain drivers like OVS, although at
          this time only vlan is supported
        + required: True
        + update_allowed: True
        + type: String
        + constraints: custom constraint 'neutron.trunk_segmentation_type'
    - segmentation_id:
        + description: The segmentation ID on which the subport network is
          presented to the instance
        + required: True
        + update_allowed: True
        + type: Integer
        + constraints: custom constraint 'neutron.trunk_segmentation_id'
* description:
    - description: A description of the trunk
    - required: False
    - type: String
    - update_allowed: True
* admin_state_up
    - description: Administrative state of the trunk
    - required: False
    - type: Boolean
    - default: True
    - update_allowed: True

Attributes:

* admin_state_up: The administrative state of the trunk
* description: Description of the trunk
* name: Name of the trunk
* port_id: ID of the trunk parent port
* revision_number: The revision number of the trunk
* sub_ports: A list of maps containing the details of port(s) associated with
  the trunk

With the above change a user can use trunks by creating a HOT template similar
to the following:

.. code-block:: yaml

  resources:
     ...
    my_trunk:
      type: OS::Neutron::Trunk
      properties:
        name: My_Trunk
        parent_port: {get_resource: my_parent_port}
        subports:
          - {port: my_subport,
            segmentation_type: vlan,
            segmentation_id: 101}
          - {port: {get_resource: my_2nd_subport},
            segmentation_type: vlan,
            segmentation_id: 102}
     ...

Neutron allows its backends to refuse trunk creation with a parent port already
bound. As of Newton and Ocata only the Open vSwitch backend has this
limitation. Other backends can create a trunk on both unbound and bound parent
ports. But with the OVS backend the trunk has to be created before the instance
is booted.

If a user wants to write backend agnostic templates and there's at least one
backend with the above limitation they should always create the trunk before
they boot the instance.

To make sure that the trunk is created first, the trunk parent port should be
referenced by ``get_attr`` as shown in the following example:

.. code-block:: yaml

  resources:
     ...
    my_instance:
      type: OS::Nova::Server
      properties:
        networks:
          port: {get_attr: [my_trunk, parent_port]}

.. note::

  The referencing method should be documented carefully as nothing prevents the
  user from assign the trunk's parent port directly to the instance, which
  would result in a missing dependency relationship.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  * nilles

Additional assignees:
  * botond-zoltan
  * etthdvi

Milestones
----------

Target Milestone for completion:
  pike-1

Work Items
----------

* Implement a new resource type: `OS::Neutron::Trunk`
* Implement a custom constraint: `neutron.trunk_segmentation_type`
* Implement a custom constraint `neutron.trunk_segmentation_id`
* Implement unit tests
* Implement functional tests
* Add sample templates to heat-templates repo
    - A template with a trunk resource and some supports
    - An example where the subport(s) and the parent port has the same MAC
      address; Explain in a comment why is this useful, refer to the
      relevant Neutron documentation [1].
* Document changes:
    - Add a release note to ``releasenotes/notes`` about the new resource type
    - Add a subsection to the Hot Template Guide about the new trunk resource,
      and explain:

        + the correct reference for the trunk: use `get_attr`
        + if a port defined as a trunk subport it may not be added to an
          instance
        + mention that the MAC addresses of the subport and the parent port may
          be the same, otherwise the user could have connectivity issues; Refer
          to the relevant Neutron documentation [1].

References:
-----------
[1]: https://github.com/openstack/openstack-manuals/blob/master/doc/networking-guide/source/config-trunking.rst#using-trunks-and-subports-inside-an-instance

Dependencies
============

None
