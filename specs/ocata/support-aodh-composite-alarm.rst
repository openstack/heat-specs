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

====================================
Support aodh composite alarm in heat
====================================

https://blueprints.launchpad.net/heat/+spec/add-aodh-composite-alarm

Adds resource plugin for Aodh composite alarm.

Problem description
===================

The combination type alarm has been deprecated in aodh, because some issues
which are hard to solved. And we have deprecated OS::Aodh::CombinationAlarm
synchronously, see:

https://blueprints.launchpad.net/heat/+spec/migrate-to-use-aodh-for-alarms

It's recommended to use composite rule alarm which is similar with the
combination alarm in functionality.


Proposed change
===============

Add the following resource under resources/openstack/aodh/

* OS::Aodh::CompositeAlarm

    * description
        Description of the alarm.
        - optional
        - type: String
        - update_allowed
    * severity
        Severity of the alarm.
        - optional
        - type: Integer
        - update_allowed
        - constraints: one of ['low', 'moderate', 'critical']
        - default: low
    * enabled
        True if alarm evaluation is enabled.
        - optional
        - type: Boolean
        - update_allowed
        - default: True
    * alarm_actions
        A list of URLs (webhooks) to invoke when state transitions to alarm.
        - optional
        - type: List
        - update_allowed
    * ok_actions
        A list of URLs (webhooks) to invoke when state transitions to ok.
        - optional
        - type: List
        - update_allowed
    * insufficient_data_actions
        A list of URLs (webhooks) to invoke when state transitions to
        insufficient-data.
        - optional
        - type: List
        - update_allowed
    * repeat_actions
        True if actions should be repeatedly notified while alarm remains
        in target state.
        - optional
        - type: Boolean
        - update_allowed
        - default: True
    * time_constraints
        Describe time constraints for the alarm.
        - optional
        - type: List
    * composite_rule
        Composite threshold rule with JSON format.
        - required
        - type: Map
        - update_allowed
        - schema: {'operator': 'or'/'and', 'rules': [rule1, rule2...]}

The following is an example of composite alarm::

  Resources:
    my_composite_alarm:
      type: OS::Aodh::CompositeAlarm
      properties:
        composite_rule:
          operator: or
          rules:
          - type: threshold
            meter_name: cpu_util
            evaluation_periods: 1
            period: 60
            statistic: avg
            threshold: 0.8
            comparison_operator: ge
            exclude_outliers: false
          - and:
            - type: threshold
              meter_name: disk.usage
              evaluation_periods: 1
              period: 60
              statistic: avg
              threshold: 0.8
              comparison_operator: ge
              exclude_outliers: false
            - type: threshold
              meter_name: mem_util
              evaluation_periods: 1
              period: 60
              statistic: avg
              threshold: 0.8
              comparison_operator: ge
              exclude_outliers: false
        description: a composite alarm
        ...... (other properties)

Alternatives
------------
None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
    huangtianhua@huawei.com

Milestones
----------
Target Milestone for completion:
  ocata-1

Work Items
----------

* Add OS::Aodh::CompositeAlarm resource
* Add related tests
* Add sample template using OS::Aodh::CompositeAlarm in heat-templates


Dependencies
============

None
