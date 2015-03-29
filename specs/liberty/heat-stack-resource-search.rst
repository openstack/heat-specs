..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Stack resource filtering, sorting and pagination
================================================

https://blueprints.launchpad.net/heat/+spec/heat-stack-resource-search

Enhance the filtering, sorting and filtering ability for resources in a given
stack.

Problem description
===================

In larger stack, heat does allow 1000 (max_resources_per_stack) by default
which is configurable, and it would help users to get the resources in a stack
if its provided with pagination, sorting and filtering abilities based on
certain resource attributes

Proposed change
===============

* Pagination :

Add Following parameters in REST API and heat CLI for enabling pagination
for given stack resources:

   * marker: Starting Resource id (default=0)
   * limit: Number of records from starting index (default=20)
   * with_count: If True (default), then provide following counts in
     response:
     - count: Total number of resources in a given stack like defined in
     https://github.com/openstack/api-wg/blob/master/guidelines/counting.rst

* Sorting :

Add Following parameters in REST API and heat CLI for sorting resources
in a given stack:

   * sort: List of resource attributes in given priority sequence.
     - Allowed attributes : created_at, updated_at, status, name
     - Default key is created_at
     - Default sorting direction is desc for created_at,
     updated_at and asc for status, name.
     - sort key value format to be aligned with API-WG
     http://git.openstack.org/cgit/openstack/api-wg/tree/guidelines/pagination_filter_sort.rst

* Filtering :

Add Following parameters in REST API and heat CLI for filtering resources in
 a given stack:

   * type: List of valid Resource type
   * status: List of valid resource statuses
   * name: Resource name
   * action: List of valid resource actions
   * uuid: List of resource uuid
   * physical_resource_id: List of physical resource id

   To support NOT condition, each of the list entry could be in the form of
   '[not:]entry' like 'not:FAILED'

Affected Resource REST API:
``/v1/​{tenant_id}​/stacks/​{stack_name}​/​{stack_id}​/resources
?<query parameters>``

Here, to provide the filtering parameters, 'filter' query parameter will be
used with it's value similarly to --filters option used in CLI.

Affected Heat CLI:
(only shown the new parameters here)
``heat resource-list [-f <KEY1=VALUE1;KEY2=VALUE2...>]
[-l <LIMIT>] [-m <ID>] [-s <KEY1:asc,KEY2,KEY3>]``

Optional arguments:
  -f <KEY1=VALUE1;KEY2=VALUE2...>, --filters <KEY1=VALUE1;KEY2=VALUE2...>
  Filter parameters to apply on returned resources. This
  can be specified multiple times, or once with
  parameters separated by a semicolon.

  -l <LIMIT>, --limit <LIMIT>
  Limit the number of resources returned.
  -m <ID>, --marker <ID>
  Only return resources that appear after the given resource ID.

  -s <KEY1:asc,KEY2,KEY3>, --sort <KEY1:asc,KEY2,KEY3>
  Sorting keys in the given precedence and sorting directions.

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

* Update Resource REST API controller with additional capabilities for
  pagination, sorting and filtering
* Update the heat CLI as described in the solution section
* Add required RPC and DB api with required micro version.
* Add required additional test cases.
* Add documentation for CLI (python-heatclient), REST API (api-sites)

Dependencies
============

None
