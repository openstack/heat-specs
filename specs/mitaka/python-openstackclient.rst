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

======================================
Heat support in python-openstackclient
======================================

https://blueprints.launchpad.net/heat/+spec/heat-support-python-openstackclient

Implement a new set of heat commands as python-openstackclient plugins.

Problem description
===================

python-openstackclient is becoming the default command line client for many
OpenStack projects. Heat would benefit from implementing all of its client
commands as python-openstackclient plugins implemented in the python-heatclient
repository.

Proposed change
===============

The intent of this spec is to identify the commands to be implemented and
establish conventions for command and argument names. This spec is not intented
to be a full and correct specification of command and argument names.
The details can be left to the code reviews for the commands themselves.

The following conventions will be adopted for argument flags:

- Commands which trigger lifecycle actions will have a --wait argument which
  polls the event list until the stack COMPLETE/FAILED event is emitted.
- Single character flags will be avoided as per the ``openstack`` convention,
  except for very common arguments such as ``--template`` ``-t``,
  ``--environment`` ``-e``
- When the stack name/ID is specified it will be the first positional argument
  after the full command names
- When the resource name is specified it will be the second positional argument
  after the stack name/ID.
- ``show`` and ``list`` commands should show an appropriate quantity of data
  by default and ``--short`` or ``--long`` arguments will display a different
  level of details.

The following ``heat`` commands will be implemented for ``openstack`` initially
suggesting these command names:

Core stack commands
-------------------

::

  heat stack-create
  openstack stack create


  heat stack-update
  openstack stack update

  heat stack-list
  openstack stack list

  heat stack-show
  openstack stack show

  heat stack-delete
  openstack stack delete

  heat output-list
  openstack stack output list

  heat output-show
  openstack stack output show

Other stack commands
--------------------

::

  heat stack-abandon
  openstack stack abandon

  heat stack-adopt
  openstack stack adopt

  heat stack-cancel-update
  openstack stack update cancel

  heat stack-preview
  openstack stack update --dry-run

  heat action-check
  openstack stack check

  heat action-resume
  openstack stack resume

  heat action-suspend
  openstack stack suspend

  heat hook-clear
  openstack stack hook clear

  heat hook-poll
  openstack stack hook poll

Resource commands
-----------------

::

  heat resource-list
  openstack stack resource list

  heat resource-metadata
  openstack stack resource metadata show

  heat resource-show
  openstack stack resource show

  heat resource-signal
  openstack stack resource signal

  heat resource-type-list
  openstack orchestration resource type list

  heat resource-type-show
  openstack orchestration resource type show

Template commands
-----------------

::

  heat template-show
  openstack stack template show

  heat template-validate
  openstack stack create --dry-run

  heat template-version-list
  openstack orchestration template version list

  heat resource-type-template
  openstack orchestration resource type show --format (hot|cfn)

Event commands
--------------

::

  heat event-list
  openstack stack event list

  heat event-show
  openstack stack event show

Software config commands
------------------------

::

  heat config-create
  openstack software config create

  heat config-delete
  openstack software config delete

  heat config-show
  openstack software config show

  heat config-list
  openstack software config list

  heat deployment-create
  openstack software deployment create

  heat deployment-delete
  openstack software deployment delete

  heat deployment-list
  openstack software deployment list

  heat deployment-metadata-show
  openstack software deployment metadata show

  heat deployment-output-show
  openstack software deployment output show

  heat deployment-show
  openstack software deployment show

Snapshot commands
-----------------

::

  heat stack-restore
  openstack stack snapshot restore

  heat stack-snapshot
  openstack stack snapshot create

  heat snapshot-delete
  openstack stack snapshot delete

  heat snapshot-list
  openstack stack snapshot list

  heat snapshot-show
  openstack stack snapshot show

Misc commands
-------------

::

  heat build-info
  openstack orchestration build-info

  heat service-list
  openstack service list (need to integrate with existing command)

Alternatives
------------

- Continue to evolve ``heat`` commands and do not implement any ``openstack``
  commands.
- Instead of implementing this inside python-heatclient, create a new project
  which depends on python-heatclient and python-openstackclient.

Implementation
==============

Assignee(s)
-----------

There are many commands to implement and implementation tasks would be easily
shared among many developers. The launchpad blueprint whiteboard will be used
to coordinate the implementation status of each command and who has assigned
themself to implement each one.

Primary assignee:
  Steve Baker <sbaker@redhat.com>
Other asignees:
  Bryan Jones <jonesbr@us.ibm.com>

Milestones
----------

Target Milestone for completion:
  mitaka-3

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

None, this is an independent piece of work
