..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


===================
Designate resources
===================
https://blueprints.launchpad.net/heat/+spec/heat-designate-resource

This blueprint adds heat resource plug-ins for OpenStack DNS as a service
(designate).

Problem description
===================

OpenStack provides DNS as a service (designate) and more details are
available at wiki https://wiki.openstack.org/wiki/Designate

In heat, resource plug-ins are not available for designate service. And this
blueprint is created to provide required plug-ins for designate service.

Proposed change
===============

Designate service provides v1 and v2 APIs[1] and it's python client[2]
provides support only for v1. So in this blueprint, v1 support is added
with following resources.

* OS::Designate::Domain

 Properties:

    * name:
        - required: True
        - type: String
        - update_allowed: False
        - description: Domain name
    * ttl:
        - required: False
        - type: int
        - update_allowed: True
        - description: Time To Live (Seconds)
    * description:
        - required: False
        - type: String
        - update_allowed: True
        - description: Description of domain
    * email:
        - required: True
        - type: String
        - update_allowed: True
        - description: Domain email

Attributes:

    * serial:
        - description: DNS domain serial

* OS::Designate::Server

Properties:

    * name:
        - required: True
        - type: String
        - update_allowed: True
        - description: DNS Server Name

* OS:Designate::Record

Properties:

    * domain:
        - required: True
        - type: String
        - update_allowed: False
        - description: DNS Domain id or name
        - constraints: CustomConstrain('designate.domain')
    * name:
        - required: True
        - type: String
        - update_allowed: False
        - description: DNS Name
    * type:
        - required: True
        - type: String
        - update_allowed: True
        - description: DNS record type
        - constraints:[A, AAAA, CNAME, MX, SRV, TXT, SPF, NS, PTR, SSHFP, SOA]
    * data:
        - required: True
        - type: String
        - update_allowed: True
        - description: DNS record data (Ip address)
    * ttl:
        - required: False
        - type: int
        - update_allowed: True
        - description: DNS record Time To Live (Seconds)
    * description:
        - required: False
        - type: String
        - update_allowed: True
        - description: Description of DNS record
    * priority:
        - required: False
        - type: int
        - update_allowed: True
        - description: DNS record priority

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Kanagaraj Manickam (kanagaraj-manickam)
  Anant Patil (ananta)

Milestones
----------

Target Milestone for completion:
  Liberty-1

Work Items
----------

* Implement proposed resource plug-ins
* Implement custom constrain for 'designate.domain'
* Add required test cases


Dependencies
============
[1] http://designate.readthedocs.org/en/latest/rest.html
[2] https://github.com/openstack/python-designateclient
