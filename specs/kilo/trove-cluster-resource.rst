..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


================================
Implement Trove cluster resource
================================

https://blueprints.launchpad.net/heat/+spec/trove-cluster-resource

Add support for Trove cluster resource which will allow to create clusters
with Heat.

Problem description
===================

Currently we can't create Trove cluster resource in Heat.

Proposed change
===============

Implement new resource type:

* OS::Trove::Cluster

  * properties

    * name (optional - defaults to self.physical_resource_name())
    * datastore_type (required)
    * datastore_version (required)
    * instance_parameters (list, required)

      * flavor (required)
      * volume_size (required)

  * attributes

    * instances (list of instances ids)
    * ip (IP of the cluster)

Alternatives
------------

None


Usage Scenario
==============

Create the OS::Trove::Cluster resource like this::

  resources:
    cluster:
      type: OS::Trove::Cluster
      properties:
        name: my_cluster
        datastore_type: mongodb
        datastore_version: 2.6.1
        instances: [{flavor: m1.heat, volume_size: 1},
                    {flavor: m1.small, volume_size: 2},
                    {flavor: m1.large, volume_size: 3}]


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  tlashchova

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

* Add Trove cluster resource


Dependencies
============

None
