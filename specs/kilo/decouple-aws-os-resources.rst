..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..


===============================
 Decouple AWS and OS resources
===============================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/decouple-aws-os-resources

Decouple AWS and OS resources code.

Problem description
===================

The code structure of the resources folder is in some confusion.
https://blueprints.launchpad.net/heat/+spec/reorganize-resources-code-structure

There is too much coupling between AWS and OS resources for reorganizing to be
possible, for example modules: wait_condition.py, instance.py, user.py and
volume.py.

Proposed change
===============

The new code structure will be::

    heat
    |----engine
         |----resources
              |----aws
                   |----wait_condition.py(AWS::CloudFormation::WaitCondition)
                   |----wait_condition_handle.py
                        (AWS::CloudFormation::WaitConditionHandle)
                   |----volume.py
                        (AWS::EC2::Volume and AWS::EC2::VolumeAttachment)
                   |----user.py(AWS::IAM::User and AWS::IAM::AccessKey)
                   |----instance.py(AWS::EC2::Instance)
              |----openstack
                   |----wait_condition.py(OS::Heat::WaitCondition)
                   |----wait_condition_handle.py(OS::Heat::WaitConditionHandle)
                   |----volume.py
                        (OS::Cinder::Volume and OS::Cinder::VolumeAttachment)
                   |----access_policy.py(OS::Heat::AccessPolicy)
                   |----ha_restarter.py(OS::Heat::HARestarter)
              |----wait_condition.py(base module)
         |----volume_tasks.py(volume attach/detach tasks)

And also the tests code will be split::

   heat
    |----engine
    |----tests
         |----test_waitcondition.py
         |----test_os_waitcondition.py
         |----test_volume.py
         |----test_os_volume.py

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
  Kilo-2

Work Items
----------

* Decouple AWS and OS WaitCondition related resources
* Decouple AWS and OS Volumes related resources
* Decouple AWS and OS Instances related resources
* Decouple AWS and OS Users related resources
* Decouple responding tests

Dependencies
============

None

