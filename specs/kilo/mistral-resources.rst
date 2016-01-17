..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


===========================
Implement Mistral resources
===========================

https://blueprints.launchpad.net/heat/+spec/mistral-resources-for-heat

Add support for Mistral resources which will allow to create and execute
workflows.

Problem description
===================

Heat doesn't support Mistral resources currently.

Mistral is a task management service, also known as Workflow as a Service.
Resources, which will be added to Heat, add new possibilities:

* Workflows, which contains different tasks for execution.
* Actions, which are a particular instructions associated with a tasks
  that needs to be performed once tasks dependencies are satisfied.
* CronTriggers, which make possible to run workflows according to
  specific rules: periodically setting a cron pattern or on external
  events like Ceilometer alarm.
* Executions, which allows to execute given Workflows.

Proposed change
===============

Mistral resources are not integrated, so they will be added to contrib
directory.
Mistral client plugin will be added for communication with Mistral, which has
his own requirements. Following resources will be added with next syntax:

Add the OS::Mistral::Workflow resource, like this:

.. code-block:: yaml

   resources:
    workflow:
      type: OS::Mistral::Workflow
      properties:
        definition: |
          workflow_name:
            type: String
            description: String
            input: [Value, Value, ...]
            output: { ... }
            on-success: [Value, Value, ...]
            on-error: [Value, Value, ...]
            on-complete: [Value, Value, ...]
            policies: { ... }
            tasks: { ... }
        input: { ... }

Where definition specifying rely on Mistral DSL v2.

Add the OS::Mistral::CronTrigger resource, like this:

.. code-block:: yaml

   resources:
     cronTrigger:
       type: OS::Mistral::CronTrigger
       properties:
         name: my_cron_trigger
         pattern: 1 0 * * *
         workflow:
           name: String
           input: { ... }

There is some use cases, which should be described:

1. To create and execute workflow follow next steps: at first we create
   template with OS::Mistral::Workflow:

   .. code-block:: yaml

      heat_template_version: 2013-05-23
      resources:
        workflow:
          type: OS::Mistral::Workflow
          properties:
            definition: |
              test:
                type: direct
                tasks:
                  hello:
                    action: std.echo output='Hello'
                    publish:
                      result: $

   When stack will created, to execute workflow run next command::

      heat resource-signal stack_name workflow_name \
          -D 'Json-type execution input'

   Execution state will be available in 'executions' attribute as a dict.

2. Compatibility with Ceilometer alarms, i.e. using webhook url for workflow
   executing:

   .. code-block:: yaml

      heat_template_version: 2013-05-23
      resources:
        workflow:
          type: OS::Mistral::Workflow
          properties:
            definition: |
              test:
                type: direct
                tasks:
                  alarm_hello:
                    action: std.echo output='Alarm!'
                    publish:
                      result: $
        alarm:
          type: OS::Ceilometer::Alarm
          properties:
              alarm:
                type: OS::Ceilometer::Alarm
                properties:
                  meter_name: cpu_util
                  statistic: avg
                  period: 60
                  evaluation_periods: 1
                  threshold: 0
                  alarm_actions:
                    - { get_attr: [workflow, alarm_url] }
                  comparison_operator: ge
      outputs:
        executions:
          value: { get_attr: [workflow, executions] }
        workflows:
          value: { get_attr: [workflow, available_workflows] }

   In the template, described above, workflow will begin execute when alarm
   will goes to the state 'alarm'. Output 'execution' contain dict with info
   about all executions, which belong to the workflow. Output 'workflows'
   contain dict with all workflows' names that belong to the workflow, e.g.
   {'test': 'stack_name.workflow.test'}.
3. Using cron trigger in template. There is the definition named 'wfdef.yaml':

   .. code-block:: yaml

      version: 2.0
        create_vm:
          type: direct
          input:
            - vm_name
            - image_ref
            - flavor_ref
          output:
            vm_id: $.vm_id
          tasks:
            create_server:
              action: >
                nova.servers_create name={$.vm_name} image={$.image_ref}
                flavor={$.flavor_ref}
              publish:
                vm_id: $.id
              on-success:
                - check_server_exists
            check_server_exists:
              action: nova.servers_get server={$.vm_id}
              publish:
                server_exists: True
              on-success:
                - wait_instance
            wait_instance:
              action: nova.servers_find id={$.vm_id} status='ACTIVE'
              policies:
                retry:
                  delay: 5
                  count: 15

   This definition will be used in template, which also have cron trigger
   resource:

   .. code-block:: yaml

      heat_template_version: 2013-05-23
      resources:
        workflow:
          type: OS::Mistral::Workflow
          properties:
            definition: { get_file: wfdef.yaml }
            input:
              vm_name: test
              image_ref: some_image_id
              flavor_ref: some_flavor_id

        cron_trigger:
          type: OS::Mistral::CronTrigger
          properties:
            name: test_trigger
            pattern: 1 0 * * *
            workflow: { get_attr: [workflow, available_workflows, create_vm]}

   Need to note, that name is optional attribute.

Alternatives
------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <prazumovsky>

Assisted by:
  <tlashchova>

Milestones
----------

Target Milestone for completion:
  Kilo-2

Work Items
----------

* Add Mistral client plugin for Heat
* Add Mistral workflow resource
* Add Mistral cron trigger resource


Dependencies
============

None
