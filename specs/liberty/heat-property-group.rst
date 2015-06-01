..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============
Property Group
==============

https://blueprints.launchpad.net/heat/+spec/heat-property-group

Adds PropertyGroup for grouping set of properties of a Heat Resource plug-in.

Problem description
===================
In many of heat resource plug-in implementation, properties are getting
defined with validation schema and there is no group concept exist
which is required for following reasons:

* some time, resource mandates to provide either PropertyA or PropertyB,
  and one of them is mandatory. This can't be defined as of now in heat
  Properties schema, as developer can't set required=true for both the
  properties and as part of validate() method, developer should implement
  the logic whether one of these property is provided.

* some of the plug-in supports multiple versions of its thing, for example,
  docker plug-in supports multiple versions. so Some properties are only
  supported in some versions only. Now there is no generic way exist to
  specify declaratively that some properties are required for a given client
  version.


Proposed change
===============
The first problem, could be solved by introducing the concept of
PropertyGroup, which helps declarative validation as defined below:

Assume that there are two Properties PropertyA and PropertyB, and are already
declared with proper Property Schema. Then Property Group could be defined as
follows:

.. code-block:: python

    properties_schema: {
        PropertyA: {},
        PropertyB: {},
        ''' Here Either of these Properties are mandatory, but required=True
        can't be defined.'''
        property_groups: [
            group1: {
                properties:[PropertyA,PropertyB],
                operator: xor
            }
        ]
    }

Here as part of 'validation()' phase, each of the groups in the property_groups
will be validated in sequence by using the operator across properties. This
helps to bring up the complex validation logic across dependent properties.

Each group declared in the property_groups can refer  the other group in it's
properties list. so the complex validation could be:

.. code-block:: python

    property_groups: [
            group1: {
                properties:[PropertyA,PropertyB],
                operator: OR
            },
            group2: {
                properties:[PropertyC,PropertyD,group1],
                operator: AND
            },
        ]

Some time, a property or property_group will be depending on another property
or property_group and this can be achieved by using 'depends_on' as one of the
operator. Here operator are one of the binary operator supported by python.

Here, each of the property entry in the group's properties field,
could be defined in the form of

    'prp1.child_prp1.grand_child_prp1'.

where the first property in this pattern is depends on where property_groups
is declared.

* TOP-LEVEL-PROPERTY-GROUP: if property_groups is declared as top
  level entry in properties_schema, then first property in the pattern
  should be one of the top level property defined in the properties_schema.

* ROOT-LEVEL-PROPERTY-GROUP:If its declared inside one of the property's
  properties_schema then the first property is consider as one of its peer
  property name.

It will help developers to declare at appropriate place.

consider below properties_schema:

.. code-block:: python

    properties_schema = {
        ROLES: properties.Schema(
            properties.Schema.LIST,
            _('List of role assignments.'),
            schema=properties.Schema(
                properties.Schema.MAP,
                _('Map between role with either project or domain.'),
                schema={
                    ROLE: properties.Schema(
                        properties.Schema.STRING,
                        _('Keystone role'),
                        required=True,
                        constraints=([constraints.
                                     CustomConstraint('keystone.role')])
                    ),
                    PROJECT: properties.Schema(
                        properties.Schema.STRING,
                        _('Keystone project'),
                        constraints=([constraints.
                                     CustomConstraint('keystone.project')])
                    ),
                    DOMAIN: properties.Schema(
                        properties.Schema.STRING,
                        _('Keystone domain'),
                        constraints=([constraints.
                                     CustomConstraint('keystone.domain')])
                    ),
                }
            ),
            update_allowed=True
        )
    }

Here either ROLE and PROJECT or ROLE and DOMAIN needs to provided for
creating the role-assignment. But both PROJECT and DOMAIN can't be
declared with required=true. so property_groups could be defined as below:

TOP-LEVEL-PROPERTY-GROUP:

.. code-block:: python

    properties_schema = {
        ...
        property_groups: [
                role-project: {
                    properties:[ROLES.ROLE,ROLES.PROJECT],
                    operator: AND
                },
                role-group: {
                    properties:[ROLES.ROLE, ROLES.GROUP],
                    operator: AND
                },
                either-group: {
                    properties:[property_groups.role-project,
                                property_groups.role-group],
                    operator: OR
                }
            ]
    }


ROOT-LEVEL-PROPERTY-GROUP

.. code-block:: python

    properties_schema = {
        ROLES: properties.Schema(
            properties.Schema.LIST,
            _('List of role assignments.'),
            schema=properties.Schema(
                properties.Schema.MAP,
                _('Map between role with either project or domain.'),
                schema={
                    ...
                    property_groups: [
                        role-project: {
                            properties:[ROLE, PROJECT],
                            operator: AND
                        },
                        role-group: {
                            properties:[ROLE, GROUP],
                            operator: AND
                        },
                        either-group: {
                            properties:[property_groups.role-project,
                                        property_groups.role-group],
                            operator: OR
                        }
                    ]

                }
            ),
            update_allowed=True
        )
    }

The second problem could be solved as follows:
PropertyGroup can be used with 'client_plugin_supported_since' as follows:

.. code-block:: python

    property_groups: [
        group1: {
            properties:[PropertyA,PropertyB],
            operator: OR
            client_plugin_supported = [1.2]
        }
    ]

Heat engine can infer that this set of properties in the PropertyGroups are
supported only from 1.2 version. so it can check the current
client_plugin_supported and  validate accordingly.

NOTE: property_groups is only declarative in resource plug-in implementation
and it does not exposed in the template definition.

Alternatives
------------
As implemented currently in each of the resource plug-in.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
    Kanagaraj Manickam (kanagaraj-manickam)
    Peter Razumovsky <prazumovsky>

Milestones
----------
Target Milestone for completion:
  liberty-1

Work Items
----------

* Define PropertyGroup class with required validation logic for the given
  resource
* Update the resource validation logic to validate with property group
* Update the existing resources with property_groups.
* Generate property group documentation for users to understand the property
  requirements.
* Add required test cases


Dependencies
============
None.