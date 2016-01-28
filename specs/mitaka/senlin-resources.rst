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
* Node - A node is an object that belongs to at most one Cluster.
* Policy - A policy is a set of rules that can be checked and/or enforced when
  an Action is performed on a Cluster.
* Receiver - A receiver is an abstract resource created at the senlin engine
  that can be used to hook the engine to some external event/alarm sources.

Proposed change
===============

Senlin client plugin and Senlin resources will be added to heat.

1. Cluster
----------

Description:
Cluster resource in senlin can create and manage objects of
the same nature, e.g. Nova servers, Heat stacks, Cinder volumes, etc.
The collection of these objects is referred to as a cluster.

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

Description:
Profile resource in senlin is a template describing how to create nodes in
cluster.

Namespace:
OS::Senlin::Profile

Required Properties:
--------------------

type:
  The type of Senlin Profile.
  String Value.
  Custom constraint 'senlin.profile_type'.


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

properties:
  Properties of Senlin profile.
  Map value.

3. Policy
---------

Description:
Policy is a set of rules that can be checked and/or enforced when
an Action is performed on a Cluster. A policy resource can be attached to
multiple clusters.

Namespace:
OS::Senlin::Policy

Required Properties:
--------------------

type:
  The type of senlin policy.
  String Value.
  Custom Constraint 'senlin.policy_type'.

Optional Properties:
--------------------

name:
  The name of the Senlin policy.
  String Value.
  Update allowed.

description:
  The description of the Senlin policy.
  String Value.

properties:
  The properties of the Senlin policy.
  Map Value.

bindings:
  The clusters this policy attach to.
  List value, [{cluster: String, enabled: Boolean}]
  Update allowed.

4. Node
-------

Description:
Node is an object that belongs to at most one Cluster, it can be created
based on a profile.

Namespace:
OS::Senlin::Node

Required Properties:
--------------------

profile:
  The name or id of senlin profile for this node.
  String Value.
  Constraint with 'senlin.profile'.
  Update allowed.

Optional Properties:
--------------------

cluster:
  The name or id of senlin cluster this node will attach to.
  String Value.
  Constraint with 'senlin.cluster'.

metadata:
  Metadata for this node.
  Map Value.
  Update allowed.

name:
  The name of this node.
  String Value.
  Update allowed.

5. Receiver
-----------

Description:
Receiver is an abstract resource created at the senlin engine
that can be used to hook the engine to some external event/alarm sources.

Namespace:
OS::Senlin::Receiver

Required Properties:
--------------------

cluster:
  The name or id of senlin cluster to attach to.
  String Value.
  Constraint with 'senlin.cluster'.

action:
  The action to be executed when receive a signal.
  String Value.
  Allowed values are [CLUSTER_SCALE_OUT, CLUSTER_SCALE_IN]

Optional Properties:
--------------------

type:
  The type of receiver.
  String Value.
  Default value is 'webhook'.
  Allowed values are ['webhook'].

name:
  Name of this receiver.
  String Value.

params:
  The parameters passed to action when receive a signal.
  Map Value.

Attributes:
-----------
actor:
  A trusts id will include in actor.
  Map value.

channel:
  A 'alarm_url' will include in channel.
  Map Value.

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
  Mikata-3

Work Items
----------

* Add Senlin client plugin for Heat
* Add OS::Senlin::Cluster resource
* Add OS::Senlin::Profile resource
* Add OS::Senlin::Policy resource
* Add OS::Senlin::Node resource
* Add OS::Senlin::Receiver resource
* Add example templates to heat-templates

Dependencies
============

None
