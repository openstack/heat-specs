..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================
Implement Zun resources
=======================

https://blueprints.launchpad.net/heat/+spec/heat-plugin-zun

This Blueprint proposes to add support for Zun resources.

Problem description
===================

Zun is a container management service that is currently not supported by
Heat. Resources will be added to Heat to support:

* Container, an application container


Proposed change
===============

Zun resources will be added to zun directory
in heat/engine/resources/openstack/zun/**
Zun client plugin will be added for communication with Zun, which has
his own requirements. Following resources will be added:

* Add the following resource plugin:

* OS::Zun::Container resource

    * name
        -type: string
        -required: false
        -update_allowed

    * image
        -type: string
        -required: true

    * command
        -type: string
        -required: false

    * cpu
        -type: int
        -required: false
        -update_allowed

    * memory
        -type: string
        -required: false
        -update_allowed

    * environment
        -type: map
        -required: false
        -default: {}

    * workdir
        -type: string
        -required: false

    * labels
        -type: map
        -required: false
        -default: {}

    * image_pull_policy
        -type: string
        -required: false
        -choices: [never, always, ifnotpresent]

    * restart_policy
        -type: string
        -required: false

   * interactive
       -type: boolean
       -required: false
       -default: false

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <sitlani.namrata@yahoo.in>


Milestones
----------

Pike

Work Items
----------

* Implement Zun client plugin for Heat
* Add Container to resources

Dependencies
============

None
