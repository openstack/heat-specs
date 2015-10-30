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

===========================
Support Nova Host Aggregate
===========================

https://blueprints.launchpad.net/heat/+spec/support-host-aggregate

Provides support for Nova Host Aggregate feature.

Problem description
===================

Nova already implemented host aggregate for host resource management.
Administrator of cloud may want to use host aggregate to further partition an
availability zone.

Proposed change
===============

1. Add following Resources under resources/openstack/nova/

* OS::Nova::HostAggregate

    * name (required, name for host aggregate)
    * availability_zone (optional, availability zone in aggregate)

      - Will apply custom constraint 'nova.availability_zone' on it.

    * hosts (optional, assign hosts in aggregate)
    * metadata (optional, a set of metadata for aggregate)

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
Rico Lin <rico-lin>

Milestones
----------

  mitaka-1

Work Items
----------

* Add resources related
* Add related tests

Dependencies
============

None
