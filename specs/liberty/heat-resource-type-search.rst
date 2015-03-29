..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================
Search Resource Type
====================

https://blueprints.launchpad.net/heat/+spec/heat-resource-type-search

Enable filtering capabilities for resource types loaded in the given heat
deployment.

Problem description
===================

Search and get resource type based on
* resource type,
* supported since,
* support status

Proposed change
===============

Add Following parameters in REST API and heat CLI for filtering heat
resource type:

   * resource_type: List of glob matching expression (like ``*``)
   * supported_since: Heat version, since resource type is supported.
   * supported_status: List of status. It could be one of UNKNOWN,
     SUPPORTED, PROTOTYPE, DEPRECATED, UNSUPPORTED

To support NOT condition, each of the list entry could be in the form of
'[not:]entry' like 'not:DEPRECATED'

Affected Service REST API:
``/v1/​{tenant_id}​/resource_types?filter=<query parameters>``
Here, 'filter' query parameter will be used with it's value similarly to
--filters option used in CLI.

Affected Heat CLI:
(only shown the new parameters here)
```heat resource-type-list [-f <KEY1=VALUE1;KEY2=VALUE2...>]``

Optional arguments:
  -f <KEY1=VALUE1;KEY2=VALUE2...>, --filters <KEY1=VALUE1;KEY2=VALUE2...>
  Filter parameters to apply on returned resource type. This
  can be specified multiple times, or once with
  parameters separated by a semicolon.


Alternatives
------------
None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
    Kanagaraj Manickam (kanagaraj-manickam)

Milestones
----------
Target Milestone for completion:
  liberty-1

Work Items
----------

* update Resource Type REST API controller with additional filtering ability.
* update the heat CLI as described in the solution section
* Add required additional test cases.
* Add documentation for CLI, REST API updates

Dependencies
============

None
