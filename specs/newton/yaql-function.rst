..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


=====================
Support YAQL function
=====================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/yaql-function

This blueprint adds support of YAQL to heat.


Problem description
===================

https://github.com/openstack/yaql

YAQL (Yet Another Query Language) is an embeddable and extensible query
language, that allows performing complex queries against arbitrary objects.

Heat currently does not have the ability to evaluate complex expressions, such
as:

  * Select values for a key from a list of dictionary.
  * Filter the list where one or more fields match condition(s).
  * Transform a list to dictionary or vice versa.
  * Simple arithmetic.
  * Evaluation of boolean logic.
  * Any combination of select, filter, transform, and evaluate.

Proposed change
===============

This spec proposes to add yaql function to the heat of the such form::

  yaql:
    expression: <expression>
    data:
        <var1>: <val1>
        ...

Where `expression` is a valid yaql expression that will be evaluated,
`data` is a dictionary with variables to which we can refer from the
`expression`.

Referencing to corresponding data::

  outputs:
    o1:
      value: {yaql: {expression: $.data.foo, data: {foo: 1}}}

o1 will be evaluated to 1

Expression evaluation::

  parameters:
    list_param:
      type: comma_delimited_list
      default: [1, 2, 3]
    bool_param1:
      type: boolean
      default true
    bool_param2:
      type: boolean
      default: false
  resources:
    asg:
      type: OS::Heat::AutoscalingGroup
      properties:
        resource:
          type: OS::Nova::Server
          ...
    rg:
      type: OS::Heat::ResourceGroup
      properties:
        count: 3
        type: child.yaml
        properties:
          index: "%index%"
          ...
  outputs:
    o1:
      yaql:
        expression: $.data.bool_param1 and $.data.bool_param2
        data:
          bool_param1: {get_param: bool_param1}
          bool_param2: {get_param: bool_param2}
    o2:
      yaql:
        expression: $.data.list_param.select(int($)).max()
        data:
          list_param: {get_param: list_param}
    o3:
      yaql:
        expression: int($.data.list_param[0]) + int($.data.list_param[1]))
        data:
          list_param: {get_param: list_param}
    o4:
      yaql:
        expression: $.values().where($.status="FAILED").select($.id)
        data: {get_attr: [asg, outputs, show]}

The content of child.yaml::

  parameters:
    nova_flavors:
      type: comma_delimited_list
      default: [m1.tiny, m1.small, m1.large]
    index:
      type: string
  resources:
    instance:
      type: OS::Nova::Server
      properties:
        ...
        flavor:
          yaql:
            expression: $.data.nova_flavors[
              int($.data.index) mod $.data.nova_flavors.len()]
            data:
              nova_flavors: {get_param: nova_flavors}
              index: {get_param: index}

o1 will be evaluated to false,
o2 will be evaluated to 3,
o3 will be evaluated to 3,
o4 will contain a list os servers id that are in failed state,
3 servers with m1.tiny, m1.small, m1.large flavors will be created.

Add 2 config options for bounding of yaql:

`limit_iterators` that defines maximum number of elements in collection that
expression can take for its evaluation, and

`memory_quota` that defines maximum size of memory in bytes that expression can
take for its evaluation.


Alternatives
------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ochuprykov@mirantis.com


Milestones
----------

  newton-1

Work Items
----------

1. Implement yaql intrinsic function.
2. Add related tests.
3. Add corresponding docs.
4. Add examples of usage to heat-templates.


Dependencies
============

None
