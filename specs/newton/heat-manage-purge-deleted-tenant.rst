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

=======================================================
Enable the purge of deleted stacks for specific project
=======================================================

Add project-id argument to heat-manage purge_deleted command in order
to be able to hard delete DB entries for a specific project.

https://blueprints.launchpad.net/heat/+spec/heat-manage-purge-deleted-tenant

Problem description
===================

Currently heat-manage purge_deleted command allows operators to purge
all DB entries marked as deleted and are older than an age.

Usually this global purge process is setup to run periodically in a
cloud platform. However, for some specific projects, cloud operators
would like to setup the purge process with much smaller retention period.
Typical example of such project is the monitoring project that monitors
heat service.

Proposed change
===============

Add project-id argument for heat-manage purge_deleted command::

  ~ # heat-manage purge_deleted --help
  usage: heat-manage purge_deleted [-h] [-g {days,hours,minutes,seconds}]
                                   [-p PROJECT_ID]
                                   [age]

  positional arguments:
     age                   How long to preserve deleted data.

  optional arguments:
    -h, --help            show this help message and exit
    -g {days,hours,minutes,seconds}, --granularity {days,hours,minutes,seconds}
                          Granularity to use for age argument,
                          defaults to days.
    -p PROJECT_ID, --project-id PROJECT_ID
                          Project ID to purge deleted stacks.

When project-id argument is set, only this project DB entries marked as deleted
will be purged. Given project-id value will not be validated, leaving
the database unchanged if incorrect.

Alternatives
------------

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ala Rezmerita <ala.rezmerita@orange.com>

Milestones
----------

Target Milestone for completion:
  newton-2

Work Items
----------

- Implement proposed change
- Add the corresponding functional tests

Dependencies
============
