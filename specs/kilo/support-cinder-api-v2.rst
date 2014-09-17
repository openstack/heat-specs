..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================
Support Cinder API version 2
============================

https://blueprints.launchpad.net/heat/+spec/support-cinder-api-v2

This specification proposes to add support for the second version of the Cinder
API, which brings useful improvements and will soon replace version one.


Problem description
===================

Currently Heat uses only version 1 of Cinder API to create volumes.  Version
two, however, brings useful features such as scheduler hints, more consistent
responses, caching, filtering, etc.

Also, Cinder is deprecating API version 1 in favor of 2 [1], which has been
available in devstack since Havana.  Supporting both would make switching
easier for users.

The new API provides [2]:

* More consistent properties like 'name', 'description', etc.
* New methods (set_metadata, promote, retype, set_bootable, etc.)
* Additional options in existing methods (such as the use of scheduler hints).
* Caching data between controllers instead of multiple database hits.
* Filtering when listing information on volumes, snapshots and backups.

Use cases:

* As a developer I want to be able to pass scheduler hints to Cinder when
  creating volumes, in order to choose back-ends more precisely.
* As a deployer I don't want to have to choose which Cinder API version to use.
  Let Heat autodiscover the latest and use it.


Proposed change
===============

Add new methods to CinderClientPlugin:

* discover_api_versions()
  To query Keystone for 'volume' and 'volumev2' services.
* api_version()
  To get the Cinder API version currently used by Heat (this value will be set
  to latest available one).

The client returned by CinderClientPlugin._create() will be made depending on
api_version().

Six cinderclient methods are currently used within Heat:

* volumes.get(), volumes.extend(), backups.create() and restores.restore() that
  won't be affected by this change;
* volumes.create() and volume.update() that use arguments that differ depending
  on the Cinder API version: (display_name, display_description) for v1 and
  (name, description) for v2.

The proposed implementation will not change current OS::Cinder::Volume
properties, since they already are 'name' and 'description' (as in new API
version).

Alternatives
------------

Wait for Cinder API v1 to be deprecated and switch abruptly to v2.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  adrien-verge

Milestones
----------

Target Milestone for completion:
  Kilo-1

Work Items
----------

* Discover the latest Cinder API version using Keystone.
* Create the correct Cinder client using the latest available API.
* Use correct arguments for volumes.create() and volume.update() depending on
  the used API.


Dependencies
============

None


References
==========

* [1]: https://wiki.openstack.org/wiki/CinderAPIv2
* [2]: https://github.com/openstack/nova-specs/blob/master/specs/juno/support-cinderclient-v2.rst
