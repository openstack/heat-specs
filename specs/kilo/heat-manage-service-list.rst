..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================
Heat-manage service list
========================

https://blueprints.launchpad.net/heat/+spec/heat-manage-service-list

Adds the ability to heat-manage command to list the running status of
heat-engines deployed in a given cloud environment.

Problem description
===================

In a given enterprise cloud environment, Heat to support horizontal scaling,
multiple heat-engines will be deployed and executed. Once these engines are
deployed on multiple hosts, there is no way an admin can find these
heat engines details like

* what is the node on which heat engine is running,
* what is the running status of each engine.
* How long the heat-engines are running successfully.


Proposed change
===============
Heat already provides heat-manage command to take care of the database syncing
and archiving. As part of this blue print, 'service list' is added to provide
the following details:

* Heat-engine node name
* Heat-engine running status
* Heat-engine host (message queue)
* Heat-engine last updated time of running status.


Alternatives
------------
None


Implementation
==============

Assignee(s)
-----------

Kanagaraj Manickam (kanagaraj-manickam)

Milestones
----------
Target Milestone for completion:
  Kilo-1

Work Items
----------

* Add required db migration script to add the new table 'Services'
* Add 'Service' model in the sqlalchemy and required db api
* Update the heat-engine service for updating the db at given periodic interval
* Add 'service list' to heat.cmd.manage and it required help
* Add heat service REST API as contrib (extension) api
* Add heat service-list command in heat CLI
* Add required test cases

Dependencies
============

None
