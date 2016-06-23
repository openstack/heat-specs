..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================
Properties Group
================

https://blueprints.launchpad.net/heat/+spec/heat-property-group

Adds PropertiesGroup for grouping set of properties of a Heat Resource plug-in.

Problem description
===================

In many of Heat resource plug-in implementations, properties are getting
defined with validation schema and there is no group concept which is required
for following reasons:

* sometimes, resource mandates to provide either PropertyA or PropertyB,
  and one of them is mandatory. This can't be defined now in Heat
  Properties schema, as developer can't set required=true for both the
  properties and as part of validate() method, developer should implement
  the logic whether one of these property is provided.

* some plug-ins supports multiple versions of its thing, for example,
  docker plug-in supports multiple versions. So some properties are only
  supported in specific versions only. Now there is no generic way to
  specify declaratively that some properties are required for a given client
  version.

Proposed change
===============

The first problem could be solved by introducing the concept of
PropertiesGroup, which helps declarative validation as defined below:

Resource class will have `properties_groups_schema`, which contains list of
properties groups. Each properties group has next representation:

Assume that there are two Properties: PropertyA and PropertyB, and there are
already declared with proper Property Schema. Then properties group will be
specified by logical expression in dict:

.. code-block:: python

    properties_groups_schema = [
        {properties_group.AND: [[PropertyA], [PropertyB]]}
    ]

In that way, logical expression consists of one-key dict with list-type value,
which can contain list-type properties names or properties group logical
expression. Dictionary key should be equal to one of the following operators:
"and", "or", "xor".

Properties groups can be nested, for example:

.. code-block:: python

   properties_groups_schema = [
       {properties_group.AND: [
           {properties_group.OR: [[PropertyA], [PropertyB]]},
           [propertyC]]}
   ]

Here as part of 'validation()' phase, each of the groups in the
property_groups_schema will be validated in sequence by using the operator
across properties. This helps to bring up the complex validation logic across
dependent properties.

Each group declared in the properties_groups_schema can refer the other group
in it's properties list. So the complex validation could be:

Here, each of the property entry could be defined in the form of

    ['prp1', 'child_prp1', 'grand_child_prp1']

even if property entry comprises only one item, i.e.

    ['prp1']

For example, if there's properties_schema:

.. code-block:: python

    properties_schema = {
        PropertyA: properties.Schema(
            properties.Schema.MAP,
            schema={
                PropertySubA: properties.Schema(properties.Schema.STRING),
                PropertySubB: properties.Schema(properties.Schema.STRING)
            }
        )
    }

Then properties_groups_schema should be next:

.. code-block:: python

    properties_groups_schema = [
        {properties_group.AND: [[PropertyA, PropertySubA],
                                [PropertyA, PropertySubB]]}
    ]

Also, properties group will support specifying API versions of `client_plugin`,
used for property, i.e. property will be supported only if specified
`client_plugin` API version satisfies versions in group. Then property group
will have next format:

.. code-block:: python

    properties_groups_schema = [
        {properties_group.API_VERSIONS: {
            properties_group.CLIENT_PLUGIN: <client_plugin object>,
            properties_group.VERSIONS: <list of supported versions>,
            properties_group.PROPERTIES: <list of properties entries>}
        }
    ]


Example of using `API_VERSIONS` as properties group:

.. code-block:: python

    properties_groups_schema = [
        {properties_group.API_VERSIONS: {
            properties_group.CLIENT_PLUGIN: self.client_plugin('keystone'),
            properties_group.VERSIONS: ['1.2', '2.0'],
            properties_group.PROPERTIES: [[PropertyA], [PropertyB]]}
        }
    ]

Heat engine can infer that this set of properties in the properties group is
supported only for 1.2 and 2.0 API versions, so it can check the current
`client_plugin` supported and validate accordingly.

Besides the validation part, all necessary changes will be added to
documentation generator to allow user learn relations between properties.

Alternatives
------------

None.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
    Kanagaraj Manickam (kanagaraj-manickam)

    Peter Razumovsky <prazumovsky>

Milestones
----------

Currently moved to backlog due to no community's interest. Workable PoC placed
here:

https://review.openstack.org/#/q/topic:bp/property-group

Work Items
----------

* Define PropertiesGroup class with required validation logic for the given
  resource
* Update the resource validation logic to validate with property group
* Update the existing resources with property_groups
* Generate property group documentation for users to understand the property
  requirements
* Add required test cases


Dependencies
============
None.
