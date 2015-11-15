..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================================
Support simple json format in os::mistral::workflow handle signal
=================================================================

https://blueprints.launchpad.net/heat/+spec/mistral-wf-signal-json-format

Currently the resource os::mistral::workflow expects a specific json format
when it is signaled (either using the alarm-url or the resource-signal API
call). Since external systems don't always enable the user to change the body
of the request they send, the workflows are not able to use the information
sent by these systems.

Problem description
===================

When signaling the OS::Mistral::Workflow resource, from an external system,
or even from ceilometer, the signaling request may have a predefined body,
which is not compatible with the json format expected by the workflow resource.
The os::mistral::workflow expects the body to be in this format:

.. code-block:: json

    {
        "input":{
        ...
        },
        "params":{
        ...
        }
    }

however, ceilometer, for example, sends this body in the request:

.. code-block:: json

    {
         "severity": "low",
         "alarm_name": "my-alarm",
         "current": "insufficient data",
         "alarm_id": "895fe8c8-3a6e-48bf-b557-eede3e7f4bbd",
         "reason": "1 datapoints are unknown",
         "reason_data": {
               "count": 1,
               "most_recent": null,
               "type": "threshold",
               "disposition": "unknown"
         },
         "previous": "ok"
    }

This causes the problem that the workflow can't use the information in the
request body.

Proposed change
===============

The suggested change is to enable the workflow resource to parse the request
body as a simple json map, where each key will be treated as an input value.

This change will not break backward compatibility as the user can choose how
the body would be parsed in the stack template.

The proposal is to add a new property "use_request_body_as_input" to
os::mistral::workflow, when this property is defined in the template and is
True, then the parsing of the signal request body will be parsed as a
simple json map. If the property is not defined or defined to False, the body
will be parsed as it always has (expecting the keys "input" and "params").

Since the external systems using this signal send a predefined request, we
can assume that they are unaware of the fact they are signaling a workflow,
and so, they don't have the need to pass "params" which is mistral workflow
specific. The params can be defined in the stack template but overriding
them using the request, will not be enabled in this case.

For example in order for a workflow resource to use information from a
ceilometer alarm, it's definition in the stack template would be something
like this:

.. code-block:: yaml

    my_workflow:
        type: OS::Mistral::Workflow
        properties:
          use_request_body_as_input: True
          input:
            current: !!null
            alarm_id: !!null
            reason: !!null
            previous: !!null
            severity: !!null
            alarm_name: !!null
            reason_data: !!null

Alternatives
------------
None

Implementation
==============

When the resource is being signaled it will check for the existence of the
"use_request_body_as_input" property and based on its definition, it will
parse the request body, to find the appropriate input values.

It is worth noting that if the workflow resource is created with the property
"use_request_body_as_input" set to True, then the workflow "params" cannot
be passed to the request.

Assignee(s)
-----------

Primary assignee:
  noa-koffman

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

1. Change workflow resource to parse the request in the appropriate way based
   on resource definition.
2. Add tests to see that both old and new functionality are working.


Dependencies
============
None