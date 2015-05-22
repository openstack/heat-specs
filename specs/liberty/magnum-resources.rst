..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
Implement Magnum resources
==========================

https://blueprints.launchpad.net/heat/+spec/magnum-resources

This Blueprint proposes to add support for Magnum resources.

Problem description
===================

Magnum is a container management service that is currently not supported by
Heat. Resources will be added to Heat to support:

* Baymodel, An object stores template information about the bay which is used
  to create new bays consistently.
* Bay, A collection of node objects where work is scheduled.
* Pod, A collection of containers running on one physical or virtual machine.
* Service, An abstraction which defines a logical set of pods and a policy
  by which to access them.
* ReplicationController, An abstraction for managing a group of PODs to
  ensure a specified number of PODs are running.
* Node, A baremetal or virtual machine where work executes
* Container, A docker container


Proposed change
===============

Magnum resources are not integrated, so they will be added to contrib
directory.

Magnum client plugin will be added for communication with Magnum, which has
his own requirements. Following resources will be added:

Add the OS::Magnum::BayModel resource

.. code-block:: yaml

   resources:
     model:
       type: OS::Magnum::BayModel
       properties:
         name: String
         image: String
         keypair: String
         external_network: String
         dns_nameserver: String
         flavor: String
         docker_volume_size: Int

Add the OS::Magnum::Bay resource

.. code-block:: yaml

   resources:
     bay:
       type: OS::Magnum::Bay
       properties:
         name: String
         baymodel: { get_resource: model }
         node_count: Int

Add the OS::Magnum::Pod resource

.. code-block:: yaml

   resources:
     pod:
       type: OS::Magnum::Pod
       properties:
         bay: { get_resource: bay }
         manifest: SOFTWARE_CONFIG
         manifest_url: String

Add the OS::Magnum::Service resource

.. code-block:: yaml

   resources:
     service:
       type: OS::Magnum::Service
       properties:
         bay: { get_resource: bay }
         manifest: SOFTWARE_CONFIG
         manifest_url: String

Add the OS::Magnum::ReplicationController resource

.. code-block:: yaml

   resources:
     rc:
       type: OS::Magnum::ReplicationController
       properties:
         bay: { get_resource: bay }
         manifest: SOFTWARE_CONFIG
         manifest_url: String

Add the OS::Magnum::Node resource

.. code-block:: yaml

   resources:
     rc:
       type: OS::Magnum::Node
       properties:
         name: String
         type: String
         image: String

Add the OS::Magnum::Container resource

.. code-block:: yaml

   resources:
     rc:
       type: OS::Magnum::Node
       properties:
         name: String
         type: String
         command: String


Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <rpothier@cisco.com>


Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

* Add Magnum client plugin for Heat
* Add Magnum BayModel and Bay resources
* Add Magnum Pod, Service and ReplicationController resources
* Add Magnum Node and Container resources

Dependencies
============

None
