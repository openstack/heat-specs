..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


===============================================================
 Support to generate hot templates based on the specified type
===============================================================

https://blueprints.launchpad.net/heat/+spec/support-to-generate-hot-templates

This Blueprint will support to generate hot templates based on the specified
type.

Problem description
===================

Currently Heat only supports to generate the 'HeatTemplateFormatVersion'
template based on the specified resource type, this is the functionality
exposed via the 'heat resource-type-template' command. And the link of the
API:

http://developer.openstack.org/api-ref-orchestration-v1.html

See resource_types/{type_name}/template API.

Proposed change
===============

The changes will support to generate hot templates based on the specified type,
since we recommend user using hot templates.

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
  Liberty-1

Work Items
----------

* Update the heat API to support passing an new option specifying
  the required template type. Return the cfn template if not specify
  the new option.
* Update python-heatclient to expose this new option.
* Add related tests for changes.

Dependencies
============

None
