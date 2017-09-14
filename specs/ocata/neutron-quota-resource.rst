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

===============================
New Neutron Quota Resource Type
===============================

https://blueprints.launchpad.net/heat/+spec/neutron-quota-resource

An administrator would like to have the ability to specify a project's
neutron quota in a HOT template. This blueprint proposes to create a new
heat resource type for neutron quotas.

Problem description
===================

Today, an administrator can create a new keystone project using heat
using a template similar to this:

.. code-block:: yaml

  resources:
    test_role:
      type: OS::Keystone::Role
      properties:
        name: test_role

    test_project:
      type: OS::Keystone::Project
      properties:
        name: test_project
        enabled: True

    test_user:
      type: OS::Keystone::User
      properties:
        name: test_user
        domain: default
        default_project: {get_resource: test_project}
        roles:
          - role: {get_resource: test_role}
            domain: default
          - role: {get_resource: test_role}
            project: {get_resource: test_project}


However, to specify the neutron quota associated with the project, the
administrator would need to execute post-orchestration something
similar to:

.. code-block:: bash

  $ os quota set --floating-ips 5 --networks 5 --subnets 5  <project>

Use Cases
---------

For an Openstack admin, it would be ideal to be able to manage projects
holistically, using templates that will define the project, the users to
project membership and the allocated quotas.

Proposed change
===============

This blueprint proposes to add a new resource type ``OS::Neutron::Quota``
to heat to address the problem described. A sample ``OS::Neutron::Quota``
template:

.. code-block:: yaml

  resources:
    neutron_quota:
      type: OS::Neutron::Quota
      properties:
        project: {get_param: project}
        floating_ips: 5
        health_monitors: 5
        members: 5
        networks: 5
        pools: 5
        ports: 5
        rbac_policies: 5
        routers: 5
        security_groups: 5
        security_group_rules: 5
        subnetpools: 5
        subnets: 5
        vips: 5
  outputs:
    neutron_quota_id:
      value: {get_resource: neutron_quota}

**Properties**:

* project:
    - **required**: True
    - **type**: String
    - **description**: OpenStack keystone project
    - **constraints**: Must be a valid keystone project
* floating_ips:
    - **type**: Integer
    - **description**:  Quota for the number of floating IPs
    - **constraints**: Range minimum is -1
* health_monitors:
    - **type**: Integer
    - **description**:  Quota for the number of health monitors
    - **constraints**: Range minimum is -1
* members:
    - **type**: Integer
    - **description**:  Quota for the number of members
    - **constraints**: Range minimum is -1
* networks:
    - **type**: Integer
    - **description**:  Quota for the number of networks
    - **constraints**: Range minimum is -1
* pools:
    - **type**: Integer
    - **description**:  Quota for the number of pools
    - **constraints**: Range minimum is -1
* ports:
    - **type**: Integer
    - **description**:  Quota for the number of ports
    - **constraints**: Range minimum is -1
* rbac_policies:
    - **type**: Integer
    - **description**:  Quota for the number of RBAC policies
    - **constraints**: Range minimum is -1
* routers:
    - **type**: Integer
    - **description**:  Quota for the number of routers
    - **constraints**: Range minimum is -1
* security_groups:
    - **type**: Integer
    - **description**:  Quota for the number of security groups
    - **constraints**: Range minimum is -1
* security_group_rules:
    - **type**: Integer
    - **description**:  Quota for the number of security group rules
    - **constraints**: Range minimum is -1
* subnetpools:
    - **type**: Integer
    - **description**:  Quota for the number of subnet pools
    - **constraints**: Range minimum is -1
* subnets:
    - **type**: Integer
    - **description**:  Quota for the number of subnets
    - **constraints**: Range minimum is -1
* vips:
    - **type**: Integer
    - **description**:  Quota for the number of vips
    - **constraints**: Range minimum is -1

A default policy rule will be added for this resource to be limited to
administrators.

.. code-block:: json

  "resource_types:OS::Neutron::Quota": "rule:project_admin"

This Quota Resource will handle create, update, and delete. For handling
create and update, the resource will call the Neutron client's quota-set update
method, since there is no quota create call. For the handling delete, the
Resource will call the Neutron client's quota delete method. This will reset
the quota to the default value. Note that creating multiple resources and
deleting one will reset the quota even though other resources still exist.

Alternatives
------------

The administrator or the operator can change a project's default quota manually
post project orchestration.

The OS::Keystone::Project can contain an optional Quota property. However,
the addition seems out of Keystone's scope, since Keystone has no concept of
quotas.

Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Yosef Hoffman - yohoffman

Additional assignees:

* Julian Sy - syjulian
* Andy Hsiang - yh418t

Milestones
----------

Target Milestone for completion:
  ocata-1

Work Items
----------

* Implement new resource type OS::Neutron::Quota
* Implement appropriate unit and functional tests

Dependencies
============

None

