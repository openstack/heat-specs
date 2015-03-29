..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================
Cinder volume encryption support
================================

https://blueprints.launchpad.net/heat/+spec/cinder-volume-encryption

Provides support for encrypted cinder volume creation.

Problem description
===================

Cinder provide encrypted volume creation by using encrypted volume type
as described in below wiki page:
http://docs.openstack.org/juno/config-reference/content/section_volume-encryption.html

Proposed change
===============

Add new contrib heat resource plugin for creating the encrypted volume type
OS::Cinder::EncryptedVolumeType with following properties:

    * provider (required)

        * description: The class that provides encryption support. For example,
          nova.volume.encryptors.luks.LuksEncryptor.
        * type: string

    * cipher (optional)

        * description: The encryption algorithm or mode. For example,
          aes-xts-plain64
        * type: string

    * key_size (optional)

        * description: Size of encryption key, in bits. For example, 128 or
          256.
        * type: integer

    * control_location (optional)

        * default: front-end
        * allowed-values: front-end, back-end.
        * description: Notional service where encryption is performed.
        * type: string

    * type (required)

        * description: Name or id of volume type (OS::Cinder::VolumeType)
        * type: string

This resource needs following actions:

    * create
    * delete

Alternatives
------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Kanagaraj Manickam (kanagaraj-manickam)

Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

* Add new contrib resource plugin as described in the solution section
* Add test cases for new resource plugin
* Add required functional test cases to validate the resource.

Dependencies
============

None