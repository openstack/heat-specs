..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


=================================
support cinder volume type manage
=================================

https://blueprints.launchpad.net/heat/+spec/cinder-volume-type

Cinder volume type is an import parameter when creating a volume, it can
specify the volume backend and specific whether support consistency group
and so on.
Support OS::Cinder::VolumeType resource manage in heat will be good.

Note that by default only users who have the admin role can manage volume
types because of the default policy in Cinder.

Problem description
===================

Currently volume types need to be managed externally to heat and passed into
the stack as parameters. This spec defines how we could create both the volume
and the volume type within one template.

Proposed change
===============

Add the OS::Cinder::VolumeType resource, like this::

  resources:
    my_volume_type:
      type: OS::Cinder::VolumeType
      properties:
        name: volumeBackend
        metadata: {volume_backend_name: lvmdriver}

Note that because of the admin restriction mentioned above,
the new resource will be added to /contrib.

Alternatives
------------

None


Usage Scenario
--------------

For volume creation take the volume_type to specific the lvm-driver::

   resources:
     my_volume:
      type: OS::Cinder::Volume
      properties:
        size: 10
        volume_type: {get_resource: my_volume_type}

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

* Add OS::Cinder::VolumeType resource, implement its basic actions
* Add UT/Tempest for the change


Dependencies
============

None
