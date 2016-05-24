..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


===================
Migrate to use Aodh
===================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/migrate-to-use-aodh-for-alarms

This blueprint will migrate to use Aodh service directly for alarm resources.


Problem description
===================

Ceilometer has moved all the alarming code and subsystem to the Aodh project:
https://review.openstack.org/#/c/196552
https://review.openstack.org/#/c/197161

Although now we can use ceilometer-client to redirect to Aodh endpoint when
creating alarm resources:
https://review.openstack.org/#/c/202938

But there are some reasons I believe we should to migrate to use
Aodh service directly:

1. Ceilometer team plans to deprecate/remove the function of redirecting,
   maybe in two releases

2. Aodh is the independent alarming service


Proposed change
===============

1. This spec proposes to use Aodh service for alarm resources.
For mostly alarm resources (except OS::Ceilometer::CombinationAlarm)
can compatible with the current implementation.

2. The problem is that we can't manage the OS::Ceilometer::CombinationAlarm
by Aodh client, because Aodh client does not support. The combination alarm
is deprecated and disabled by default in Aodh, and the new composite rule
alarm is recommended to use. So this spec proposes to deprecate
OS::Ceilometer::CombinationAlarm and to add the new composite rule
alarm resource plug-in named 'OS::Aodh::CompositeAlarm'


Alternatives
------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  huangtianhua@huawei.com
  liusheng@huawei.com


Milestones
----------

  newton-2

Work Items
----------

1. Add Aodh client plugin.

2. Migrate to use Aodh service to manage the alarm resources's lifecycle,
   including threshold alarm , composite alarm, gnocchi_resources_threshold
   alarm, gnocchi_aggregation_by_metrics_threshold alarm and
   gnocchi_aggregation_by_resources_threshold alarm.

3. Set resource_registry to map Ceilometer alarms to Aodh alarms, to make
   sure older templates with Ceilometer alarms still work.

4. Add corresponding tests.

5. Modify all related docs with word 'Ceilometer'.


Dependencies
============

None
