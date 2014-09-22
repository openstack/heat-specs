..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode
..

=======================================
 Reorg AutoScalingGroup Implementation
=======================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/reorg-asg-code

This specs is about reorganize AutoScalingGroup implementation which includes
the following resource types:

  - AWS::AutoScaling::LaunchConfiguration
  - AWS::AutoScaling::AutoScalingGroup
  - AWS::AutoScaling::ScalingPolicy
  - OS::Heat::InstanceGroup
  - OS::Heat::AutoScalingGroup
  - OS::Heat::ScalingPolicy
  - OS::Heat::ResourceGroup

The goal is to 1) reorganize the class hierarchy; 2) split and relocate sources
into subdirectories to better reflect resources' name space; 3) make it easier
for future enhancements to each resource types.

Problem description
===================

The current class hierarchy of resource groups and scaling groups is something
like the diagram shown below::

  CooldownMixin
   |
   | StackResource
   |   |
   |   +--> ResourceGroup [OS::Heat::ResourceGroup]
   |   |
   |   +--> InstanceGroup [OS::Heat::InstanceGroup]
   |         |
   +---------+--> AutoScalingGroup [AWS::AutoScaling::AutoScalingGroup]
   |                |
   |                +--> AutoScalingResourceGroup [OS::Heat:AutoScalingGroup]
   |
   | SignalResponder
   |   |
   +---+--> ScalingPolicy [AWS::AutoScaling::ScalingPolicy]
              |
              +--> AutoScalingPolicy [OS::Heat::ScalingPolicy]

Besides this hierarchy, there are utility functions located in the modules like
heat.scaling.template.

One of the problems of this design is related to namespace as pointed out by
an existing blueprint:

https://blueprints.launchpad.net/heat/+spec/resource-package-reorg

Another problem is that having all classes implemented in almost one file is
making the implementation difficult to digest or improve.  For example, it
may make a better sense to have InstanceGroup a subclass of ResourceGroup.
For another example, it doesn't make much sense to have AutoScalingResourceGroup
a subclass of InstanceGroup because the subclass is more open to other resource
types as its members.

Proposed change
===============

1. Reorganize Class Hierarchy

The proposed change is to reorganize the class hierarchy to be something like
shown in the diagram below::

  CooldownMixin
   |                           StackResource
   |                                  |
   |                            ResourceGroup
   |                       [OS::Heat::ResourceGroup]
   |                                  |
   |              +-------------------+---------------+
   |              |                                   |
   +-->    AutoScalingGroup                      InstanceGroup
   | [OS::Heat::AutoScalingGroup]          [OS::Heat::InstanceGroup]
   |                                                  |
   |                                                  |
   +---------------------------------------> AWSAutoScalingGroup
   |                                 [AWS::AutoScaling:AutoScalingGroup]
   |
   |                 SignalResponder
   |                        |
   +----------------------->|
                            |
                +-------------------------------+
                |                               |
        AWSAutoScalingPolicy             AutoScalingPolicy
   [AWS::AutoScaling::ScalingPolicy]  [OS::Heat::ScalingPolicy]


This change will break the subclass relationships between OpenStack and AWS
implementation.

As for utility/helper classes, e.g. `CooldownMixin`, the first step is to
separate them into independent classes, followed by further refactoring them
into utility functions when appropriate.

2. Relocate Source Files

The AWS version will be relocated into heat/engine/resources/aws subdirectory,
including the LaunchConfiguration implementation.  The OpenStack version will
be relocated into heat/engine/resources/openstack subdirectory.

The shared parent class ResourceGroup will remain in heat/engine/resources, while
the CooldownMixin class will be relocated into heat/scaling subdirectory.  The
eventual layout of the modules and classes would look like this::

  heat/engine/resources/
    |
    +-- resource_group.py  [ResourceGroup]
    +-- instance_group.py [InstanceGroup]
    |
    +-- aws/
    |    |
    |    +--- autoscaling_group.py [AWSAutoScalingGroup]
    |    +--- scaling_policy.py [AWSAutoScalingPolicy]
    |    +--- launch_config.py [LaunchConfiguration]
    |
    +-- openstack/
         |
         +-- autoscaling_group.py [AutoScalingGroup]
         +-- scaling_policy.py [AutoScalingPolicy]

  heat/scaling/
    |
    +-- cooldown.py [CooldownMixin]
    +-- (possibily other shared utility classes)


This reshuffling is optional.  We will determine whether reshuffling is necessary
indeed after the cleanup work is done.

Alternatives
------------

Since this is a pure implementation level change, one rule of thumb is that "we
don't break userland".

We can have AWS AutoScalingPolicy extend Heat AutoScalingPolicy.  However that
may mean that any future changes to Heat implementation must be very careful, in
case those changes may break the conformance of the AWS version to its Amazon
specification.

The same applies to the two versions of AutoScalingGroup.  Hopefully, we may
extract common code into ResourceGroup level to minimize code duplication.
However, having a subclass relationship between these two classes is not a
good design in the long term.  The goal of the AWS version is to closely
follow the Amazon development while the goal of the Heat version is more
about user needs in the context of OpenStack.  So the current thought is to
split the implmentation although it may imply some code duplication.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Qiming

There could be other contributors interested in helping out as well.

Milestones
----------

Target Milestone for completion:
  Kilo-1

Work Items
----------

- Extract common code to parent classes
- Split AWS version and OS version of resources
- Modify test cases

Dependencies
============

No new dependencies to other libraries will be introduced.

This work may disturb several on-going work related to AutoScalingGroups.
The following work will have to be rebased on this change.

#. https://review.openstack.org/110379 Scaling group scale-down plugpoint
#. https://review.openstack.org/105644 LaunchConfiguration bdm
#. https://review.openstack.org/105907 Balancing ScalingGroup across AZs

