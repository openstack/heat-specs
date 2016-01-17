..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Implement 'InstanceId' for LaunchConfiguration
==============================================

https://blueprints.launchpad.net/heat/+spec/implement-instanceid-for-launchconfiguration

We should support the 'InstanceId' for AWS::AutoScaling::LaunchConfiguration
resource to be compatible with AWSCloudFormation.

Problem description
===================

In AWSCloudFormation, user can specify 'InstanceId' property if he wants the
launch configuration to use settings from an existing instance, see:

http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html
http://docs.aws.amazon.com/AutoScaling/latest/DeveloperGuide/create-lc-with-instanceID.html

Will be good to implement 'InstanceId' property to be compatible with
AWSCloudFormation.


Proposed change
===============
1. Add 'InstanceId' property, optional and non-updatable
2. Change 'ImageId' and 'InstanceType' properties to optional
3. Add the validation of 'InstanceId', 'ImageId' and 'InstanceType', if don't
   specify 'InstanceId', the other two properties are required
4. According to the aws developer guide and implementation, allows three cases:

 * Without 'InstanceId', should specify 'ImageId' and 'InstanceType'
   properties, using the old way to create the new launch configuration.

 * Specify 'InstanceId' only, the new launch configuration has
   'ImageId', 'InstanceType', 'KeyName', and 'SecurityGroups'
   attributes from the instance.

 * Specify 'InstanceId' and other properties else, these properties will
   override the attributes from the instance.


Alternatives
------------
None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
huangtianhua <huangtianhua@huawei.com>

Milestones
----------
Target Milestone for completion:
  Kilo-1

Work Items
----------

* Support the 'InstanceId' property
* Add UT/Tempest for the change

Dependencies
============

None
