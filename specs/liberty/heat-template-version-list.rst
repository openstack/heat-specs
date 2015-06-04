..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
Heat template versions list
===========================

https://blueprints.launchpad.net/heat/+spec/template-version-list

Add an ability to get list of available template versions by
REST API and CLI

Problem description
===================

There is no such command in heat now. It is useful for helping
end-users to write heat templates, especially for HOT builders.
Another use-case is to get list of available template versions that
are available on current deployment.

Proposed change
===============

Add the following command to heat CLI:

``heat template-version-list``

Output may be the following:

+--------------------------------------+-----+
| Versions                             |Type |
+======================================+=====+
| heat_template_version.2013-05-23     |hot  |
+--------------------------------------+-----+
| heat_template_version.2014-10-16     |hot  |
+--------------------------------------+-----+
| heat_template_version.2015-04-30     |hot  |
+--------------------------------------+-----+
| HeatTemplateFormatVersion.2012-12-12 |cfn  |
+--------------------------------------+-----+
| AWSTemplateFormatVersion.2010-09-09  |cfn  |
+--------------------------------------+-----+

Corresponding REST API would be the following:

``GET on /template_versions``

Alternatives
------------
None


Implementation
==============

Assignee(s)
-----------

ochuprykov
tlashchova
skraynev

Milestones
----------
Target Milestone for completion:
  liberty-1

Work Items
----------

* Update REST API controller with additional capabilities
* Update the heat CLI
* Add required RPC
* Add required additional test cases.
* Add documentation for CLI (python-heatclient), REST API (api-sites)

Dependencies
============

None
