..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================
Special form of get_attr which returns all attributes
=====================================================

https://blueprints.launchpad.net/heat/+spec/get-attr-all-attributes

Add new functionality for ``get_attr`` function which allows to return dict of
all attributes.

Problem description
===================

Current implementation of base attribute "show" returns JSON
representation of resource. Content of this representation depends on
particular resource. This output is also used in native clients for building
output of command :code:`<client> <resource name>-show`.

Historically some Heat resources have attributes schema with attributes
taken from the output mentioned above. However it doesn't mean,
that all attributes in schema are presented in "show" output.
It's mostly related to dynamic attributes and custom attributes,
which require additional calculations, e.g. "addresses" attribute
of OS::Nova::Server that also contains related port id in output.

From the other side Heat also have resources with empty attribute schema,
so only "show" attribute is available for them.

In some cases to avoid using several outputs in template it will be useful
to return all attributes from attribute schema
(excluding the base attribute "show") in one output.
This functionality should be added for ``get_attr`` intrinsic function.

Proposed change
===============

Add some special form of ``get_attr`` as next::

 { get_attr: [resource_name] }

with no extra arguments, which will returns dict of all attributes' outputs.

This behaviour of get_attr can be used only when the latest
heat_template_version is selected, so this case should be noted in the
documentation.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <prazumovsky>

Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

* Add new functionality to ``get_attr``
* Add note to documentation about new functionality of ``get_attr``


Dependencies
============

None
