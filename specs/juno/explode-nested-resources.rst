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

=============================
Explode Nested Resources
=============================

https://blueprints.launchpad.net/heat/+spec/explode-nested-resources

For many UI use-cases, it is generally resource intensive to list all
resources associated with a given stack if that stack includes stack-based
resources. It is therefore proposed that `resource-list` should return all
resources associated with a given stack if requested.

Problem description
===================

Currently, `resource-list` only returns top-level resources of a given stack
but does not include resources that are inside of any nested stacks. This
makes several use cases difficult or sub-optimal because of the need to make
several API calls on resource reference links.

* When deleting a stack, a UI should be able to present the user with a list
  of *all* resources associated with a given stack to avoid confusion about
  what and why certain resources were deleted due to a stack delete.
* A user of the API (either via CLI, curl, or other method) wants to be able
  to quickly and easily list and follow the status of every resource associated
  with a stack, regardless of a resource's position in the stack hierarchy.
* OpenStack dashboard may show an incorrect, confusing topology of resources
  from a stack because it knows nothing about a nested stack (e.g. a group of
  servers).

Proposed change
===============

The proposed implementation would add an optional query parameter to the
`resource-list` API method:

nested_depth
  Recursion depth to limit the returned resources. This parameter
  indicates that the user wishes to return nested resources as well as those
  from the parent stack. Setting this parameter to a number results in the
  system limiting the recursion depth. A value of `0` has no effect. A value
  of `MAX` results in all resources being returned up to
  `max_nested_stack_depth`. The system will never recurse farther than
  `max_nested_stack_depth`, regardless of the value passed in the parameter.

The Heat service would see this parameter and recurse through all of the
nested stacks to the specified depth and flatten the resource list data
structure. For resources that exist in nested stacks, the containing nested
stack id and parent resource name would also be included.

The resulting response data would look like::

  {"resources":
    [
      {
        "resource_name": "db",
        "links": [...],
        "logical_resource_id": "db",
        "resource_status_reason": "state changed",
        "updated_time": "2014-04-15T18:23:35Z",
        "required_by": ["web_nodes"],
        "resource_status": "CREATE_COMPLETE",
        "physical_resource_id": "4974985c-da78-444b-aeb3-9a80baccdd1a",
        "resource_type": "OS::Trove::Instance"
      },
      {
        "resource_name": "lb",
        "links": [...],
        "logical_resource_id": "lb",
        "resource_status_reason": "state changed",
        "updated_time": "2014-04-15T18:30:52Z",
        "required_by": [],
        "resource_status": "CREATE_COMPLETE",
        "physical_resource_id": "229145",
        "resource_type": "Rackspace::Cloud::LoadBalancer"
      },
      {
        "resource_name": "web_nodes",
        "links": [...],
        "logical_resource_id": "web_nodes",
        "resource_status_reason": "state changed",
        "updated_time": "2014-04-15T18:25:10Z",
        "required_by": ["lb"],
        "resource_status": "CREATE_COMPLETE",
        "physical_resource_id": "c3a46e6f-f999-4f9b-a797-3043031d381a",
        "resource_type": "OS::Heat::ResourceGroup"
      },
      {
        "resource_name": "web_node1",
        "links": [...],
        "logical_resource_id": "web_node1",
        "resource_status_reason": "state changed",
        "updated_time": "2014-04-15T18:25:10Z",
        "required_by": ["lb"],
        "resource_status": "CREATE_COMPLETE",
        "physical_resource_id": "c3a46e6f-f999-4f9b-a797-3043031d3811",
        "resource_type": "Rackspace::Cloud::Server",
        "parent": "web_nodes",
        "nested_stack_id": "1234512345"
      },
      {
        "resource_name": "web_node2",
        "links": [...],
        "logical_resource_id": "web_node2",
        "resource_status_reason": "state changed",
        "updated_time": "2014-04-15T18:25:10Z",
        "required_by": ["lb"],
        "resource_status": "CREATE_COMPLETE",
        "physical_resource_id": "c3a46e6f-f999-4f9b-a797-3043031d3822",
        "resource_type": "Rackspace::Cloud::Server",
        "parent": "web_nodes",
        "nested_stack_id": "1234512345"
      }
    ]
  }

These changes will primarily reside in:

* heat.engine.service
* heat.db
* heat.api
* python-heatclient

Alternatives
------------

Currently, each resource that abstracts a nested stack will include a link to
the nested stack when viewed with a `resource-show`. This allows a user to
implement this functionality client-side by:

#. listing all of the resources in the stack
#. retrieving each resource individually
#. if the current resource has a link to a nested stack, recurse the resources
   of that stack and add them to the list/tree

While this offers greater flexibility in how nested resources are listed for
the user's particular use case, its very inefficient for the stated use cases
as well as very noisy from a network perspective. This specification does not
intend to remove this option, only to provide an alternative to more
efficiently satisfy several common use cases while maintaining the existing
link traversal method for use cases requiring more control over the display
of the resource hierarchy.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  randall-burt

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

* Update DB API and implementation to accept the `nested_depth` parameter
  for resource list and use that in logic to append resources from any
  nested stacks.
* Update the engine to accept and then pass the `nested_depth` parameter to
  the DB API.
* Update the API to accept and pass the `nested_depth` parameter to the
  engine; try not to have to version the RPC API, please.
* Update python-heatclient to expose the new flag and properly format the
  output
* Add the parameters to the Heat V1 WADL


Dependencies
============

None
