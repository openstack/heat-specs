..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
Implement Senlin resources
==========================

https://blueprints.launchpad.net/heat/+spec/senlin-resources

This Blueprint proposes to add support for Senlin resources.

Problem description
===================

Senlin is a generic clustering service that is currently not supported by
Heat. Resources will be added to Heat to support:

* Cluster - A cluster can manage a collection of nodes.
* Profile - Senlin supports object creation, deletion and update via a concept
  called Profile. Each profile is in essential a driver to communicate with
  certain services for object manipulation.

Proposed change
===============

Senlin client plugin and Senlin resources will be added to heat.

1. Cluster
----------

Namespace:
OS::Senlin::Cluster

Required Properties:
--------------------

profile:
  The name or id of the Senlin profile.
  String Value.
  Will apply custom constraint 'senlin.profile' on it.
  Update allowed.


Optional Properties:
--------------------

name:
  The name of the Senlin's cluster.
  String Value.
  Update allowed.

min_size:
  Minimum number of resources in the cluster.
  Integer Value.
  Update allowed.

max_size:
  Maximum number of resources in the cluster.
  Integer Value.
  Update allowed.

desired_capacity:
  Desired initial number of resources in cluster.
  Integer Value.
  Update allowed.

metadata:
  Metadata key-values defined for cluster.
  Map Value.
  Update allowed.

timeout:
  The number of seconds to wait for the cluster actions.
  Integer Value.
  Update allowed.

2. Profile
----------

Namespace:
OS::Senlin::Profile

Required Properties:
--------------------

spec:
  The spec template content for Senlin profile.[1]_
  String Value.


Optional Properties:
--------------------

name:
  The name of the Senlin profile.
  String Value.
  Update allowed.

metadata:
  Metadata key-values defined for profile.
  Map Value.
  Update allowed.

.. [1] An example spec for senlin: https://github.com/lynic/templates/blob/master/senlin/template/senlin-profile.yaml

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ethan Lynn <xjunlin@cn.ibm.com>


Milestones
----------

Target Milestone for completion:
  Mikata-1

Work Items
----------

* Add Senlin client plugin for Heat
* Add OS::Senlin::Cluster resource
* Add OS::Senlin::Profile resource

Dependencies
============

* https://review.openstack.org/#/c/227158/ Add python-senlinclient to global requirements
