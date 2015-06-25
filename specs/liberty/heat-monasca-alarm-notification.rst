..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


==================================================
Resource plugin for Monasca Alarm and Notification
==================================================

https://blueprints.launchpad.net/heat/+spec/support-monasca-alarm-notification

Adds resource plugin for Monasca Alarm and Notification

Problem description
===================

OpenStack provides monitoring-as-a-service (monasca) and more details are
available at wiki https://wiki.openstack.org/wiki/Monasca
In heat, resource plug-ins are not available for monasca service. And this
blueprint is created to provide required plug-ins for monasca alarm and
notification.

Proposed change
===============

Add following resource plugins:

* OS::Monasca::Alarm:

    * name
        - type: string
        - required: false
        - default: physical_resource_name
        - update_allowed: false
        - description:

    * description
        - type: string
        - required: false
        - update_allowed: true

    * expression
        - type: string
        - required: true
        - update_allowed: true

    * match_by
        - type: string
        - required: false
        - update_allowed: true

    * severity
        - type: list
        - required: false
        - update_allowed: true
        - allowed_values: [low, medium, high, critical]
        - default: low

    * alarm_actions
        - type: list
        - required: false
        - update_allowed: true
        - List item constrains: Custom constrain 'monasca.notification'

    * ok_actions
        - type: list
        - required: false
        - update_allowed: true
        - List item constrains: Custom constrain 'monasca.notification'

    * undetermined_actions
        - type: list
        - required: false
        - update_allowed: true
        - List item constrains: Custom constrain 'monasca.notification'

* OS::Monasca::Notification:

    * name
        - type: string
        - required: false
        - default: physical_resource_name
        - update_allowed: false

    * type
        - type: string
        - required: true
        - update_allowed: true
        - allowed_values: [email, webhook, pagerduty]

    * address
        - type: string
        - required: true
        - update_allowed: true

* Custom constrain 'monasca.notification'

As monasca provides Notification separated from the Alarm,
to be compatible with other existing alarm resources in heat,
following additional resource is added, where all actions are considered as
webhook.

If the user provided webhook is not exist in the monasca,
heat will create new notification with that webhook, before creating the
alarm, otherwise, the existing notification for that webhook will be used.

* OS::Monasca::AlarmI:

    * name
        - type: string
        - required: false
        - default: physical_resource_name
        - update_allowed: false
        - description:

    * description
        - type: string
        - required: false
        - update_allowed: true

    * expression
        - type: string
        - required: true
        - update_allowed: true

    * match_by
        - type: string
        - required: false
        - update_allowed: true

    * severity
        - type: list
        - required: false
        - update_allowed: true
        - allowed_values: [low, medium, high, critical]
        - default: low

    * alarm_actions
        - type: list
        - required: false
        - update_allowed: true
        - List item constrains: Webhook URL

    * ok_actions
        - type: list
        - required: false
        - update_allowed: true
        - List item constrains: Webhook URL

    * undetermined_actions
        - type: list
        - required: false
        - update_allowed: true
        - List item constrains: Webhook URL

* All of these resource plugins will be supported from version '5.0.0'

Alternatives
------------
None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  duanlg@live.cn
  kanagaraj-manickam

Milestones
----------

Target Milestone for completion:
  Liberty-1

Work Items
----------

* Implement Monasca client plugin
* Implement custom constrain 'monasca.notification'
* Implement alarm and notification resource plugins as detailed above
* Implement the logic to load the monsaca resources only when
  python-monascaclient is available.
* Implement required test cases.
* Add sample template in the heat-templates github repo.

Dependencies
============
None
