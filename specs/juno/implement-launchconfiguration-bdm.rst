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

=========================================================================
 Implement BlockDeviceMappings for AWS::AutoScaling::LaunchConfiguration
=========================================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/implement-launchconfiguration-bdm

We should support the BlockDeviceMappings for
AWS::AutoScaling::LaunchConfiguration resource to be compatible with
AWSCloudFormation. And therefore, user can specify volumes to attach
to instances while AutoScalingGroup/InstanceGroup creation.

Problem description
===================

Now in Heat, the AWS::AutoScaling::LaunchConfiguration resource doesn't
implement 'BlockDeviceMappings' property to indicate the volumes to be
attached. There are two problems:

1. First, it's incompatible with AWSCloudFormation. In AWSCloudFormation,
'BlockDeviceMappings' support the 'SnapshotId', user can specify a snapshot,
then a volume will be created from the snapshot, and the volume will be
attached to the instance.

http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html

2. Second, user can't specify volumes to be attached to instances which in
AutoScalingGroup/InstanceGroup while creation.

So, we should support the 'BlockDeviceMappings' for
AWS::AutoScaling::LaunchConfiguration.

Proposed change
===============

1. Implement 'BlockDeviceMappings' property for
   AWS::AutoScaling::LaunchConfiguration resource, specially in which user can
   specify the 'SnapshotId'.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <huangtianhua>

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

1. Support the BlockDeviceMappings for AWS::AutoScaling::LaunchConfiguration
   resource
2. Add UT/Tempest for the change
3. Add a template for AWS::AutoScaling::LaunchConfiguration with
   BlockDeviceMappings

Dependencies
============

https://blueprints.launchpad.net/heat/+spec/implement-ec2instance-bdm
