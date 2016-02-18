..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


===========================
Support Conditions function
===========================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/support-conditions-function

This blueprint will provide the ability to create resource conditionally.


Problem description
===================

http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html

AWS CloudFormation supports conditions function, it decides which
resources are created or not based on the result of the condition.
The conditions function is very useful of reusing templates, with conditions,
user can create different sets of resources in different contexts(such as a
test environment versus a production environment) with same template.

Heat currently does not have the ability, the user needs many templates to
satisfy their requirements, it makes templates management become much
more complex.


Proposed change
===============

Considering the user habits and compatibility with AWS CloudFormation, this
proposal will use the same style as CloudFormation for conditions function.
An example of conditions function using a hot template::

  heat_template_version: 2016-04-08

  parameters:
    env_type:
      type: string
      default: 'test'
      allowed_values: ['prod', 'test']

  conditions: {
    'for_prod': {equals: [{get_param: env_type}, 'prod']}
  }

  resources:
    server:
      type: OS::Nova::Server
      properties:
        image: cirros-0.3.0-x86_64-disk
        flavor: m1.small
    floating_ip:
      type: OS::Nova::FloatingIP
      condition: 'for_prod'
      properties:
        pool: public
    floating_ip_attachment:
      type: OS::Nova::FloatingIPAssociation
      condition: 'for_prod'
      properties:
        server_id: {get_resource: server}
        floating_ip: {get_resource: floating_ip}

  outputs:
    floating_ip:
      value: {get_resource: floating_ip}
      condition: 'for_prod'

As template above only if in 'prod' environment, we create a floating ip
and associate it to the server, and also give the output of floating ip.
In 'test' environment, we create the server only. By passing the parameter
'env_type' we can conditionally create resources for different context.

1. Add optional section Conditions/conditions for cfn/hot template.
In this section we define the conditions map, something like::

  conditions: {
    condition_name1: {Intrinsic function},
    condition_name2: {Intrinsic function},
    condition_name3: {Intrinsic function}
  }

2. Implement related condition intrinsic functions, such as
equals/not/and/or/if:

  equals: [value1, value2]
  not: [{condition}]
  and: [{condition1}, {condition2}, {...}]
  or: [{condition1}, {condition2}, {...}]
  if: [condition_name, value_if_true, value_if_false]

Notes: the details we can see the aws doc:
http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-conditions.html

3. Add optional section Condition/condition in resource/outputs section
for cfn/hot template. The value of the Condition/condition should be
condition_name which defined in 'conditions' map. If the condition result
is True, the resource/output will be created, otherwise the resource/output
will be ignored.


Alternatives
------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  huangtianhua@huawei.com


Milestones
----------

  mitaka-3

Work Items
----------

1. Implement condition intrinsic functions.
2. Add Conditions/conditions map define for cfn/hot template.
3. Implement conditionally create resource with condition.
4. Implement conditionally given output with condition.
5. Add related tests.


Dependencies
============

None
