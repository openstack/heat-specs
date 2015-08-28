..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Resources docstrings improvements
=================================

https://blueprints.launchpad.net/heat/+spec/docstring-improvements

Current Resources' descriptions are poor. Description of any resource
get from resource's class docstring. So there is need to add docstring to
resources, which have no description and fix existing relying on
`PEP rules <http://legacy.python.org/dev/peps/pep-0008/>`_.

Problem description
===================

Current Resources' descriptions are poor. It's means that new users cannot
open documentation, learn for what this or that resource is needed and begin
to use it. They have to search native documentation of resources. So,
documentation *must* contains summary information about each resource that
orchestration uses.

Besides that, some docstrings have template example, also template displays
in documentation, so there are two template's entry for one resource. This
situation should be fixed.

Proposed change
===============

Solution of this problem includes next cases:

 1. Fix all existing docstrings relying on
    `PEP rules <http://legacy.python.org/dev/peps/pep-0008/>`_. When this case
    will be done, need to remove ignorance of PEP8 rules in tox.ini file.

 2. Add docstrings of next resources:

    * OS::Barbican::* resources
    * OS::Ceilometer::* resources
    * OS::Cinder::Volume
    * OS::Cinder::VolumeAttachment
    * OS::Designate::* resources
    * OS::Heat::AccessPolicy
    * OS::Heat::AutoScalingGroup
    * OS::Heat::InstanceGroup
    * OS::Heat::SwiftSignal
    * OS::Heat::SwiftSignalHandle
    * OS::Heat::WaitCondition
    * OS::Heat::WaitConditionHandle
    * OS::Mistral::CronTrigger
    * OS::Mistral::Workflow
    * OS::Nova::FloatingIP
    * OS::Nova::FloatingIPAssociation
    * OS::Nova::Server
    * OS::Sahara::* resources
    * OS::Swift::Container
    * OS::Trove::Cluster
    * OS::Zaqar::Queue

 3. Expand/fix docstrings of next resources:

    * OS::Cinder::EncryptedVolumeType
    * OS::Cinder::VolumeType
    * OS::Glance::Image
    * OS::Heat::RandomString
    * OS::Heat::Stack
    * OS::Heat::ScalingPolicy
    * OS::Keystone::* resources
    * OS::Magnum::BayModel
    * OS::Manila::ShareNetwork
    * OS::Monasca::AlarmDefinition
    * OS::Monasca::Notification
    * OS::Neutron::* resources
    * OS::Nova::Flavor
    * OS::Nova::ServerGroup
    * OS::Trove::Instance

As additional issue, fix coding of internal templates, i.e. add tags for
YAML code for colorization template.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <prazumovsky>

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

* Fix docstrings with PEP8 rules
* Remove ignored rules from tox.ini
* Add docstrings to Resource's classes where they omitted
* Improve and fix docstring where it needed
* Fix coding of internal templates

Dependencies
============

None
