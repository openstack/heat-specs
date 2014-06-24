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

======================================================
 Implement BlockDeviceMappings for AWS::EC2::Instance
======================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/implement-ec2instance-bdm

We should support the BlockDeviceMappings for AWS::EC2::Instance resource
to be compatible with AWSCloudFormation.

Problem description
===================

Now in Heat, the AWS::EC2::Instance resource only has 'Volumes' property to
indicate the volumes to be attached, but there are two ways defining volumes
in AWSCloudFormation, 'Volumes' and 'BlockDeviceMappings', see:

http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html

1. 'Volumes' support the 'volume_id', user can specify the volume to be attached
   to the instance. This way has been implemented in Heat, but it's not a good way
   for batch creation because one volume can't be attached to many instances.

2. 'BlockDeviceMappings' support the 'snapshot_id', user can specify a snapshot,
   then a volume will be created from the snapshot, and the volume will be attached
   to the instance. This way is a good way for batch creation.

Nova supports to create a server with a block device mapping:

http://docs.openstack.org/api/openstack-compute/2/content/ext-os-block-device-mapping-v2-boot.html

So, we should support the 'BlockDeviceMappings' for AWS::EC2::Instance resource.

Proposed change
===============

1. Add 'BlockDeviceMappings' property for AWS::EC2::Instance resource,
   specially in which user can specify the 'snapshot_id'.

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

1. Support the BlockDeviceMappings for AWS::EC2::Instance resource
2. Add UT/Tempest for the change
3. Add a template for AWS::EC2::Instance with BlockDeviceMappings

Dependencies
============

None
