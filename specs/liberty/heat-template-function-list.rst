..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================
Heat template functions list
============================

https://blueprints.launchpad.net/heat/+spec/template-function-list

Add an ability to get the list of available functions for given template
by REST API and CLI

Problem description
===================

There is no possibility to get the list of functions that are supported by
the given template version. It is useful for helping template
writers, especially for HOT builders.

Proposed change
===============

Add following command to heat CLI:

``heat template-function-list <template_version>``

Where `template_version` is template version given by
`heat template-version-list` command output. This command returns
the list of available template versions with corresponding type
(cfn or hot) for user convenience.

Corresponding REST API would be the following:

``GET on /template_versions/<template_version>/functions``

Possible output:

+--------------+--------------------------------------------------------+
| Functions    |Description                                             |
+==============+========================================================+
| Fn::GetAZs   |Returns the Availability Zones within the given region. |
+--------------+--------------------------------------------------------+
| get_param    |A function for resolving parameter references.          |
+--------------+--------------------------------------------------------+
| get_resource |A function for resolving resource references.           |
+--------------+--------------------------------------------------------+
| Ref          |A function for resolving parameter references.          |
+--------------+--------------------------------------------------------+
| ...          |                                                        |
+--------------+--------------------------------------------------------+

Alternatives
------------
None

Implementation
==============
Needed template can be obtained by template manager via
_get_template_extension_manager() from template module. Each
template has the list of functions as class attribute. Description
of each functions will be obtained via __doc__() method of the
function class. Additional changes is needed to REST API controller
and RPC.

Assignee(s)
-----------

ochuprykov
tlashchova
skraynev

Milestones
----------
Target Milestone for completion:
  liberty-2

Work Items
----------

* Update Resource REST API controller with additional capabilities
* Update the heat CLI
* Add required RPC
* Add required additional test cases.
* Add documentation for CLI (python-heatclient), REST API (api-sites)

Dependencies
============

https://blueprints.launchpad.net/heat/+spec/template-version-list

