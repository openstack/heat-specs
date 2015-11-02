..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..
 This template should be in ReSTructured text. The filename in the git
 repository should match the launchpad URL, for example a URL of
 https://blueprints.launchpad.net/heat/+spec/awesome-thing should be named
 awesome-thing.rst .  Please do not delete any of the sections in this
 template.  If you have nothing to say for a whole section, just write: None
 For help with syntax, see http://sphinx-doc.org/rest.html
 To test out your formatting, see http://www.tele3.cz/jbar/rest/rest.html

============================
Designate Zone and RecordSet
============================

https://blueprints.launchpad.net/heat/+spec/heat-designate-recordset-zone

Adds support for designate v2 RecordSet and Zone.

Problem description
===================

OpenStack provides DNS as a service (designate) and more details are
available at wiki https://wiki.openstack.org/wiki/Designate

In heat, resource plug-ins are not available for designate Zone and RecordSet.
And this blueprint is created to provide these required plug-ins.

Proposed change
===============

* OS::Designate::Zone

 Properties:

    * name:
        - required: True
        - type: String
        - update_allowed: False
        - description: Zone name
    * ttl:
        - required: False
        - type: int
        - update_allowed: True
        - description: Time To Live (Seconds) and is applicable only to Zone
          of type SECONDARY.
    * description:
        - required: False
        - type: String
        - update_allowed: True
        - description: Description of zone
    * email:
        - required: True
        - type: String
        - update_allowed: True
        - description: Zone email and is applicable only to Zone of type
          SECONDARY
    * type:
        - required: False
        - type: String
        - update_allowed: False
        - description: Zone type
        - default: 'PRIMARY'
        - constraints: ['PRIMARY', 'SECONDARY']
    * masters
        - required: False
        - type: List
        - update_allowed: True
        - description: List of master name-servers and is applicable only to
          Zone of type SECONDARY

Attributes:

    * serial:
        - description: Zone serial number
        - type: String

* OS::Designate::RecordSet

Properties:

    * zone:
        - required: True
        - type: String
        - update_allowed: False
        - description: DNS zone id or name
        - constraints: CustomConstrain('designate.zone')
    * name:
        - required: True
        - type: String
        - update_allowed: False
        - description: DNS Name
    * type:
        - required: True
        - type: String
        - update_allowed: False
        - description: DNS record type
        - constraints:[A, AAAA, CNAME, MX, SRV, TXT, SPF, NS, PTR, SSHFP, SOA]
    * records:
        - required: True
        - type: List
        - update_allowed: True
        - description: DNS records
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

* Custom Constraint 'designate.zone'
    Validate the designate zone id or name

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  kanagaraj-manickam
  rh-s

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

* Implement proposed resource plug-ins and custom constraints
* Add required test cases
* Add sample templates in heat-templates

Dependencies
============

None
