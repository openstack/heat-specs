===========================
map-merge-function
===========================

https://blueprints.launchpad.net/heat/+spec/map-merge-function

Create a simple Heat intrinsic function to help merge maps.

Problem description
===================

Heat template users (TripleO) would like the ability to merge
maps into a single map. This will help with composability with
map data constructs for configuration settings.

Proposed change
===============

Add a new Heat intrisic function called map_merge which takes a
list of maps as an argument. The function will merge the list of
maps into a single map. Values in latter maps override those in
earlier ones.

Alternatives
------------

Users could write their own functions (API version) and or create a custom
Heat resource to do something similar.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  dan-prince

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

-add tests
-create function
-update docs

Dependencies
============

None.

We are very interested in making use of this function within TripleO Heat
Templates to help with composability of config settings.
