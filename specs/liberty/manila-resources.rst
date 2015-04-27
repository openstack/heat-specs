..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


==========================
Implement Manila resources
==========================

https://blueprints.launchpad.net/heat/+spec/add-manila-resources

Add support for Manila resources in Heat.

Manila provides the management of shared or distributed filesystems
(e.g. NFS, CIFS). Using Manila we can create following resources:

  * Share - unit of storage with a protocol, a size, and an access list;
  * Share type - administrator-defined "type of service";
  * Share network - tenant-defined object that informs Manila about the
    security and network configuration for a group of shares;
  * Security service - set of options that defines a security domain for
    a particular shared filesystem protocol.

Problem description
===================

Heat doesn't support Manila resources currently.

Proposed change
===============

Add Manila client plugin and implement following resource types:

1. OS::Manila::Share

  Properties:

  * share_protocol (required, one of: NFS, CIFS, GlusterFS, HDFS)
  * size (required)
  * snapshot (optional)
  * name (optional)
  * metadata (optional)
  * share_network (optional)
  * description (optional)
  * share_type (required)
  * is_public (optional, defaults to False)
  * access_rules (list, optional)

    * access_to (optional)
    * access_type (optional, one of: ip, domain)
    * access_level (optional, one of: ro, rw)

  Attributes:

  * availability_zone
  * host
  * export_locations
  * share_server_id
  * created_at
  * status

2. OS::Manila::ShareType

  Properties:

  * name (required)
  * driver_handles_share_servers (required, one of true/1, false/0)
  * is_public (optional, defaults to True)

3. OS::Manila::ShareNetwork

  Properties:

  * neutron_network (optional)
  * neutron_subnet (optional)
  * nova_network (optional)
  * name (optional)
  * description (optional)
  * security_services (list, optional)

  Attributes:

  * segmentation_id
  * cidr
  * ip_version
  * network_type

4. OS::Manila::SecurityService

  Properties:

  * type (required, one of: ldap, kerberos, active_directory)
  * dns (optional)
  * server (optional)
  * domain (optional)
  * user (optional)
  * password (optional)
  * name (optional)
  * description (optional)

Alternatives
------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  tlashchova

Assisted by:
  ochuprykov
  kkushaev

Milestones
----------

Target Milestone for completion:
  Liberty-1

Work Items
----------

* Add Manila client plugin for Heat
* Add Manila share resource
* Add Manila share network resource
* Add Manila share type resource
* Add Manila security service


Dependencies
============

None
