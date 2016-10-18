..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================================================
Update OS::Nova::Flavor Resource Type to Support Multi-project private flavors
==============================================================================

https://blueprints.launchpad.net/heat/+spec/nova-flavor-resource

An administrator would like the ability to associate a flavor with multiple
projects that are not the one's creating the flavor. This blueprint proposes
an update to an existing resource type, nova flavor.

Problem description
===================

The traditional OS::Nova::Flavor allows the definition of a private
flavor, but it only associates the flavor with the project making
the request. This change allows the resource type to be used by an
Admin user to associate a private flavor with multiple projects that
are not the one's creating the flavor.

This feature becomes necessary in a large Openstack cloud operator where
there might be dozens or hundreds of regions. Managing flavors manually
across multiple regions becomes untenable. The notion of building tools that,
via orchestrating, help manage this largely distributed environment is what
the purpose of this enhancement is.

Proposed change
===============

This blueprint proposes to alter an existing resource type ``OS::Nova::Flavor``
in heat to address the problem described. This will be done by taking the
existing ``flavor.py`` and updating the resource type.

From that file we will add ``PROJECTS`` to the list of ``PROPERTIES`` as well
as its schema. The schema will look something like:

.. code-block:: python

    PROJECTS: properties.Schema(
        properties.Schema.LIST,
        _('List of projects.'),
        update_allowed=True,
        default=None
    )

Alternatives
------------

An alternative would be to add the association to each project manually.

Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Chris Martin - cm876n

Additional Assignees:

* Tanvir Talukder - tanvirt


Milestones
----------

Target Milestone for completion:
  ocata-2

Work Items
----------

* Implement changes to resource type OS::Nova::Flavor
* Implement unit and functional tests
* Document changes to existing resource type


Dependencies
============

None
