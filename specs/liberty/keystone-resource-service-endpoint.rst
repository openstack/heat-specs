..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================
Keystone Resource plugin for Service and Endpoint
=================================================

https://blueprints.launchpad.net/heat/+spec/keystone-resource-service-endpoint

Adds resource plugin for Keystone Service and Endpoint.

Problem description
===================

In Heat based cloud deployment tool such as TripleO, vendors are automating
the creation of Keystone Region, Service and Endpoint by some-means such as
shell scripting. This is being repeated across multiple vendors and it could
automated by heat template if heat provides Resource plugin for Keystone
Region, Service and endpoint. So this blueprint is created to provide Heat
resource plugin for Keystone Service and Endpoint.

Proposed change
===============

Add following Resources under contirb/heat_keystone by using keystone v3 API.

* OS::Keystone::Service

    * name (optional - defaults to self.physical_resource_name()
    * description (optional)
    * type (required)

* OS::Keystone::Endpoint

    * region (optional)
    * service_id (required)
    * interface: 'public', 'admin' or 'internal'
    * url (required)


Alternatives
------------
None


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

* Add contrib resources for those resources defined in solution section
* Add constrains for service
* Add required test cases
* Add sample templates in heat-template project

Dependencies
============

None
