..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Keystone Resource plugin for Domain and Region
==============================================

https://blueprints.launchpad.net/heat/+spec/heat-keystone-region-resource
https://blueprints.launchpad.net/heat/+spec/heat-keystone-domain-resource

Adds resource plugin for Keystone Domain and Region.

Problem description
===================

Heat does not provide resource plugins for keystone domain and region, which
help operator to bring the hierarchical structure in cloud user organization
and service deployment respectively. This blueprint is added to support them.

Proposed change
===============

Add following resource plugins for keystone v3 Domain and Region

* OS::Keystone::Region

 Properties:

    * id:
        - required: True
        - type: String
        - update_allowed: False
        - description: Region id
    * description:
        - required: False
        - type: String
        - update_allowed: True
        - description: Description of region
    * parent_region:
        - required: False
        - type: String
        - update_allowed: True
        - description: If the region is hierarchically a child of another
          region, set this parameter to the ID of the parent region.
        - constraints: Custom Constrain 'keystone.region'
    * enabled:
        - default: True
        - type: Boolean
        - update_allowed: True
        - description: If true, the region is enabled. If false, the region is
          disabled.

* Update OS::Keystone::Endpoint to put it under given region with custom
  constraint 'keystone.region'.

* OS::Keystone::Domain

 Properties:

    * name:
        - required: True
        - type: String
        - update_allowed: True
        - description: Domain name
    * description:
        - required: False
        - type: String
        - update_allowed: True
        - description: Description of domain
    * enabled:
        - default: True
        - type: Boolean
        - update_allowed: True
        - description: If true, the domain is enabled. If false, the domain is
          disabled.

NOTE: OS::Keystone::User, OS::Keystone::Project and OS::Keystone::Group are
already having reference to custom constraint 'keystone.domain'.


Alternatives
------------
None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
    kanagaraj-manickam
    sirushtim

Milestones
----------
Target Milestone for completion:
  mitaka-1

Work Items
----------

* Add required custom constraints and resource plugins defined above.
* Add required test cases
* Add sample templates in heat-template project

Dependencies
============

None