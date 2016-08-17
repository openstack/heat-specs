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

============================
New Nova Quota Resource Type
============================

https://blueprints.launchpad.net/heat/+spec/nova-quota-resource

An administrator would like to have the ability to specify a project's nova
quota and a project user's nova quota in a HOT template. This blueprint
proposes to create a new heat resource type for nova quotas.

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


However, to specify the nova quota associated with the project, the
administrator would need to execute post-orchestration something similar to:

.. code-block:: bash

  $ os quota set --cores 5 --ram 51200 <project>
  $ nova quota-update --user <user> --floating-ips 20 <project>

Use Cases
---------

For an Openstack admin, it would be ideal to be able to manage projects
holistically, using templates that will define the project, the users to
project membership and the allocated quotas of projects and users.

Proposed change
===============

This blueprint proposes to add a new resource type ``OS::Nova::Quota``
to heat to address the problem described. A sample ``OS::Nova::Quota``
template:

.. code-block:: yaml

  resources:
    nova_user_quota:
      type: OS::Nova::Quota
      properties:
        project: {get_param: project}
        user: {get_param: user}
        cores: 5
        fixed_ips: 5
        floating_ips: 5
        instances: 5
        injected_files: 5
        injected_file_content_bytes: 5
        injected_file_path_bytes: 5
        key_pairs: 5
        metadata_items: 5
        ram: 5
        security_groups: 5
        security_group_rules: 5
        server_groups: 5
        server_group_members: 5

  outputs:
    nova_user_quota_id:
      value: {get_resource: nova_user_quota}

**Properties**:

* project:
    - **required**: True
    - **type**: String
    - **description**: OpenStack keystone project
    - **constraints**: Must be a valid keystone project
* user:
    - **type**: String
    - **description**: OpenStack keystone user
    - **constraints**: Must be a valid keystone user
* cores:
    - **type**: Integer
    - **description**:  Quota for the number of cores
    - **constraints**: Range minimum is -1
* fixed_ips:
    - **type**: Integer
    - **description**:  Quota for the number of fixed IPs
    - **constraints**: Range minimum is -1
* floating_ips:
    - **type**: Integer
    - **description**:  Quota for the number of floating IPs
    - **constraints**: Range minimum is -1
* instances:
    - **type**: Integer
    - **description**:  Quota for the number of instances
    - **constraints**: Range minimum is -1
* injected_files:
    - **type**: Integer
    - **description**:  Quota for the number of injected files
    - **constraints**: Range minimum is -1
* injected_file_content_bytes:
    - **type**: Integer
    - **description**:  Quota for the number of injected file content bytes
    - **constraints**: Range minimum is -1
* injected_file_path_bytes:
    - **type**: Integer
    - **description**:  Quota for the number of injected file path bytes
    - **constraints**: Range minimum is -1
* key_pairs:
    - **type**: Integer
    - **description**:  Quota for the number of key pairs
    - **constraints**: Range minimum is -1
* metadata_items:
    - **type**: Integer
    - **description**:  Quota for the number of metadata items
    - **constraints**: Range minimum is -1
* ram:
    - **type**: Integer
    - **description**:  Quota for the amount of ram (in megabytes)
    - **constraints**: Range minimum is -1
* security_groups:
    - **type**: Integer
    - **description**:  Quota for the number of security groups
    - **constraints**: Range minimum is -1
* security_group_rules:
    - **type**: Integer
    - **description**:  Quota for the number of security group rules
    - **constraints**: Range minimum is -1
* server_groups:
    - **type**: Integer
    - **description**:  Quota for the number of server groups
    - **constraints**: Range minimum is -1
* server_group_members:
    - **type**: Integer
    - **description**:  Quota for the number of server group members
    - **constraints**: Range minimum is -1

If a user is provided, then the user's quota for that project will be
updated. Otherwise, the project's quota will be updated.

A default policy rule will be added for this resource to be limited to
administrators.

.. code-block:: json

  "resource_types:OS::Nova::Quota": "rule:project_admin"

This Quota Resource will handle create, update, and delete. For handling
create and update, the resource will call the Nova client's quota-set update
method, since there is no quota create call. For the handling delete, the
Resource will call the Nova client's quota delete method. This will reset the
quota to the default value. Note that creating multiple resources and deleting
one will reset the quota even though other resources still exist.

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

* Implement new resource type OS::Nova::Quota
* Implement appropriate unit and functional tests

Dependencies
============

None

