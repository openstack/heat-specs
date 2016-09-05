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

==============================
New Cinder Quota Resource Type
==============================

https://blueprints.launchpad.net/heat/+spec/cinder-quota-resource

An administrator would like the ability to specify a project's default
cinder quota in HOT template. This blueprint proposes to create a new heat
resource type for cinder volume quotas.

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


However, to specify the default cinder quota associated with the project,
the administrator would need to execute post-orchestration something
similar to:

.. code-block:: bash

  $ cinder --os-volume-api-version 2 quota-update --gigabytes <num_gb> \
  --volumes <num_volumes> <project_id>

Use Cases
---------

As an Openstack admin, I would like to manage projects holistically. Templates
that will define the project, the users to project membership and the allocated
quotas.

Proposed change
===============

This blueprint proposes to add a new resource type ``OS::Cinder::Quota``
to heat to address the problem described.  A sample ``OS::Cinder::Quota``
template:

.. code-block:: yaml

  resources:
    cinder_quota:
      type: OS::Cinder::Quota
      properties:
        project: {get_param: project}
        gigabytes: {get_param: num_gigabytes}
        volumes: {get_param: num_volumes}
        snapshots: {get_param: num_snapshots}

  outputs:
    cinder_quota_id:
      value: {get_resource: cinder_quota}

**Properties**:

* project:
    - **required**: True
    - **type**: String
    - **description**: OpenStack keystone project
* gigabytes:
    - **required**: True
    - **type**: Integer
    - **description**:  Quota for the number of disk spaces (in Gigabytes)
    - **contraints**: Range minimum is -1
* volumes:
    - **required**: True
    - **type**: Integer
    - **description**: Quota for the number of volumes
    - **contraints**: Range minimum is -1
* snapshots:
    - **required**: True
    - **type**: Integer
    - **description**: Quota for the number of snapshots
    - **contraints**: Range minimum is -1

We will add a default policy rule for this resource to be limited to
administrators.

.. code-block:: json

  "resource_types:OS::Cinder::Quota": "rule:project_admin"

This Quota Resource will handle create, update, and delete. For handling
create and update, the resource will call the Cinder client's quota-set update
method, since there is no quota create call. For the handling delete, the
Resource will call the Cinder client's quota delete method. This will reset the
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

* Julian Sy - syjulian

Additional assignees:

* Yosef Hoffman - yohoffman
* Andy Hsiang - yh418t

Milestones
----------

Target Milestone for completion:
  newton

Work Items
----------

* Implement new resource type OS::Cinder::Quota
* Implement appropriate unit and functional tests
* Document the new resource type

Dependencies
============

None
