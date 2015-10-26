..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


============================================
Config option to enable observer/get_reality
============================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/flag-to-enable-observe-reality

The convergence architecture requires a observer feature which will
observe the reality for stacks. Make the observer optional till it is
developed and tested thoroughly.

Problem description
===================

To keep Heat aware of reality (changes happening in the cloud),
observers are needed. They will be responsible for observing the changes
in reality and notifying the changes. Heat will take appropriate action
based on the feedback received from observer.

The development of observer feature should not interfere with the
existing Heat code base. A config option is needed in heat.conf to
enable observer. Just like the enable_convergence flag, this flag will
be used for development and testing of observer feature in Heat.


Proposed change
===============

Add a config option that allows observer to be enabled.


Alternatives
------------

None.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ananta
  <folks interested>


Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

Implement the config option.

Dependencies
============

None.
