..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================
Implement 'InstanceId' for AutoScalingGroup
===========================================

https://blueprints.launchpad.net/heat/+spec/implement-instanceid-for-autoscalinggroup

We should support the 'InstanceId' for AWS::AutoScaling::AutoScalingGroup
resource to be compatible with AWSCloudFormation.

Problem description
===================

In AWSCloudFormation, user can specify 'InstanceId' property if he want to
create an Auto Scaling group that uses an existing instance instead of
a launch configuration, see:

http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html

Now in Heat, the AWS::AutoScaling::AutoScalingGroup resource only has
'LaunchConfigurationName' property, will be good to implement 'InstanceId'
property.


Proposed change
===============
1. Change 'LaunchConfigurationName' to be an optional property
2. Add 'InstanceId' property, optional and non-updatable
3. Add validate for AWS::AutoScaling::AutoScalingGroup resource, make sure
   choose one of the two properties
4. Modify the _get_conf_properties() function

   * if specify 'InstanceId', to get the attributes of the instance, and
     to make a temporary launch config resource, and then return the resource
     and its properties.

     Note that the attributes include ImageId, InstanceType, KeyName,
     SecurityGroups.

   * if without 'InstanceId', using the old way to get the launch config
     resource and its properties.

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
