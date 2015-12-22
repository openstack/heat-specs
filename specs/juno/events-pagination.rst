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

=============================
 Events pagination
=============================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/events-pagination

This adds support to the events index call for limit, marker,
sort_keys and sort_dir query parameters, allowing users of the API to
retrieve a subset of events.

Problem description
===================

It is now highly probable that a event-list call could
end up attempting to return hundreds of events(especially for
AutoScalingGroup resources). At a certain point Heat
starts responding with a 500 error because the response is too large.

Proposed change
===============

We should support event pagination with limit and marker query parameters.
And we should also support event sorting with sort_keys and sort_dir query
parameters. It will make the use of more convenient for event-list.

* limit: the number of events to list
* marker: the ID of the last item in the previous page
* sort_keys: an array of fields used to sort the list, 'event_time'
  or 'resource_status', default by 'event_time'
* sort_dir: the direction of the sort, 'asc' or 'desc', default is 'desc'

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <huangtianhua>

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

* Add support for pagination and sorting events
* Add UT fot the pagination and sorting events
* Add support for pagination and sorting events in python-heatclient
* Write tempest api orchestration and scenario test to exercise events
  pagination

Dependencies
============

None
