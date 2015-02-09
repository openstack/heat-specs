..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


======================================
Support Ceilometer alarm Gnocchi rules
======================================

https://blueprints.launchpad.net/heat/+spec/ceilometer-gnocchi-alarm

Gnocchi provides two new kind of Ceilometer alarm rules that allows to query
Gnocchi API instead of Ceilometer API to retreive statistics about Ceilometer
monitored metrics.

This blueprint proposes to add the corresponding heat resources:

 * OS::Ceilometer::GnocchiResourcesAlarm
 * OS::Ceilometer::GnocchiMetricsAlarm

Problem description
===================

It's now possible to send Ceilometer samples to Gnocchi in additional of the
traditional database and to create alarms that query Gnocchi API instead of
Ceilometer API to retreive statistics. But currently we can't create this
kind of alarm with heat, this BP will solve this issue.

Proposed change
===============

Add the OS::Ceilometer::GnocchiResourcesAlarm like this::

  resources:
    type: OS::Ceilometer::GnocchiResourcesAlarm
    properties:
      description: Scale-down if the average CPU < 15% for 1 minutes
      metric: cpu_util
      aggregation_method: mean
      granularity: 300
      evaluation_periods: 1
      threshold: 1
      comparison_operator: lt
      alarm_actions:
        - {get_attr: [web_server_scaledown_policy, alarm_url]}
      resource_type: instance
      resource_constraint:
        str_replace:
          template: 'server_group=stack_id'
          params:
            stack_id: {get_param: "OS::stack_id"}


Add the OS::Ceilometer::GnocchiMetricsAlarm like this::

  resources:
    type: OS::Ceilometer::GnocchiMetricsAlarm
    properties:
      description: Scale-down if the average CPU < 15% for 1 minutes
      metrics: ["09ff6ad8-1704-4f18-8989-6559307dfe79",
                "dea49e52-be42-4c71-bd77-fe265b1b6dbb"]
      aggregation_method: mean
      granularity: 300
      evaluation_periods: 1
      threshold: 1
      comparison_operator: lt
      alarm_actions:
        - {get_attr: [web_server_scaledown_policy, alarm_url]}


These resources will start to live in /contrib and will move
into the supported resources when gnocchi will move into openstack namespace
after k-3.

Alternatives
------------

None


Usage Scenario
==============

I want to create a autoscaling group that scale down when a statistics against
cpu_util of a group of vm computed by Gnocchi, reach a certain threshold::

  resources:
    type: OS::Ceilometer::GnocchiResourcesAlarm
    properties:
      description: Scale-down if the average CPU < 15% for 1 minutes
      metric: cpu_util
      aggregation_method: mean
      granularity: 300
      evaluation_periods: 1
      threshold: 1
      comparison_operator: lt
      alarm_actions:
        - {get_attr: [web_server_scaledown_policy, alarm_url]}
      resource_type: instance
      resource_constraint:
        str_replace:
          template: 'server_group=stack_id'
          params:
            stack_id: {get_param: "OS::stack_id"}

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Mehdi Abaakouk <sileht@redhat.com>

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

* Add the new Ceilometer alarm resources

Dependencies
============

None

Links
=====

* https://review.openstack.org/#/c/153291/
