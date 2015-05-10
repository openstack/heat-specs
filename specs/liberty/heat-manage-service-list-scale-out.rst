..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Scale-out and pid support for Manage Service listing
====================================================

https://blueprints.launchpad.net/heat/+spec/heat-manage-service-list-scale-out

Adds pagination, sorting and filtering capability to 'Manage service'
listing feature. In addition, each engine will be reported with pid.

Problem description
===================

In a scale out environment, cloud provider start to run many heat-engines
to serve the huge requests at the given point in time. Once many engines are
started to run, 'Manage service' would help cloud provider to find out the
currently running heat-engines and their status and they would expect to
retrieve these engines details with pagination and want to search them for a
given host on which engines are running, based on the status of them, etc.
These functionalities are missing in the current release.

Proposed change
===============

* Pagination :

Add following parameters in REST API and heat CLI for enabling pagination
for listing heat-engines as part of 'Manage Service' feature:

   * marker: Starting heat-engine service id
   * limit: Number of records from starting index (default=20)
   * with_count: If True (default), then provide following counts in
     response:
     - count: Total number of heat-engines like defined in
     https://github.com/openstack/api-wg/blob/master/guidelines/counting.rst

* Sorting :

Add following parameters in REST API and heat CLI for sorting heat-engine
services in a given heat deployment:

   * sort: List of service attributes in given priority sequence.
     - Allowed attributes : created_at, updated_at, status, hostname
     - Default key is created_at
     - Default sorting direction is desc for created_at and updated_at and
     for other allowed attributes, it will be asc.
     - sort key value format to be aligned with API-WG
     http://git.openstack.org/cgit/openstack/api-wg/tree/guidelines/pagination_filter_sort.rst

* Filtering :

Add following parameters in REST API and heat CLI for filtering heat-engine
services:

   * hostname: List of heat-engines hostname
   * status: List of heat-engines service status

To support NOT condition, each of the list entry could be in the form of
'[not:]entry' like 'not:FAILED'


Affected Service REST API:
``/v1/​{tenant_id}​/services?<above mentioned parameters as http query
parameters>``
Here, to provide the filtering parameters, 'filter' query parameter will be
used with it's value similarly to --filters option used in CLI.

Affected Heat CLI:
(only shown the new parameters here)
``heat service-list [-f <KEY1=VALUE1;KEY2=VALUE2...>]
[-l <LIMIT>] [-m <ID>] [-s <KEY1:asc,KEY2,KEY3>]``

Optional arguments:
  -f <KEY1=VALUE1;KEY2=VALUE2...>, --filters <KEY1=VALUE1;KEY2=VALUE2...>
  Filter parameters to apply on returned heat-engine services. This
  can be specified multiple times, or once with
  parameters separated by a semicolon.

  -l <LIMIT>, --limit <LIMIT>
  Limit the number of heat-engine services returned.
  -m <ID>, --marker <ID>
  Only return heat-engines that appear after the given ID.

  -s <KEY1:asc,KEY2,KEY3>, --sort <KEY1:asc,KEY2,KEY3>
  Sorting keys in the given precedence and sorting directions.

* heat-engine PID:
  In addition, When multiple heat-engines are running on a given host, it is
  difficult to find out the process-id for a given heat-engine. This is
  required during trouble shooting issues. So new field called 'pid' to be
  added to Service model.

* heat-manage service list:
  Add the similar enhancement done in CLI, (this is required for admin, when
  all heat-engines are down and heat service-list became in-capable.)

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
* DB model changes:

  * Update Service table with new column named 'pid'

* DB API changes:

  * 'service_get_all' to be updated to handle with pagination parameters and
    filtering parameters

* Object changes:

  * Add pid and corresponding changes for db api changes in the Service object
    methods

* RPC API changes:

  * Enhance 'list_services' to handle pagination and filtering capabilities

* Heat engine service:

  * Enhance the method 'service_manage_report' in EngineService to update the
    pid of current engine.

* REST API changes:

* Update ServiceController 'index' to handle pagination and filtering
  capabilities

* heat CLI:

  * 'heat service-list' to handle pagination and filtering capabilities

* heat-manage command:

  * Add the similar enhancement done in CLI.

* Add required test cases

* Documentation:

  * update documentation for REST API (api-sites), heat CLI (python-heatclient)
    and heat-manage tool

Dependencies
============

None
