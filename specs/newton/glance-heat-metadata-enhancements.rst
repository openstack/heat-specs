..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Enhance Heat Orchestration Over Glance Metadata
================================================

`bp glance-heat-metadata-enhancements
<https://blueprints.launchpad.net/heat/+spec/glance-heat-metadata-enhancements>_`

This extends Heat's orchestration abilities to include user-defined
key/value pairs.  This blueprint can be viewed as an extension of blueprint
`heat-glance-image-tag-support
<https://blueprints.launchpad.net/heat/+spec/heat-glance-image-tag-support>_`.


Problem description
===================

While Heat currently orchestrates many Glance image properties, its support is
incomplete. Specifically, Glance's ability to add key/value properties to an
image at upload-time is not exposed to the HOT author.  These properties might
be used by other OpenStack components and drivers interfacing with Glance, and
are also useful for operators to learn more about the images
themselves.

Proposed change
===============

Modify OS::Glance::Image to allow for user-defined key/values.  This properties
schema would have the following entry added:

.. code-block:: python

    PROPERTY: properties.Schema(
        properties.Schema.MAP,
        _('Arbitrary properties to associate with the image.'),
        update_allowed=True,
        default={}
        )

As this blueprint is meant to expose Glance's --property flag, the above schema
entry provides the form `property: {key1: value1, key2: value2, ...}` to the
template author.

Alternatives
------------

Users wishing to apply currently unsupported metadata would need to do it after
the stack has been deployed.

Implementation
==============

Within heat/engine/resources/openstack/glance/image.py, both the PROPERTIES and
properties_schema variables would need to be modified to handle key/value
pairs.  Particularly, these key/values would be implemented as a properties
schema map.  The handle_create() method would also be extended to pass the
`metadata` map to the Glance client via client.images.update. A handle_update()
method will also be implemented to avoid potentially expensive recreation of
large images.

Assignee(s)
-----------

Primary assignee:
    Jaime Guerrero, <jg3755@att.com, jaimguer>

Other contributors:
    Rusty Eddy, <ge363p@att.com>

Milestones
----------

newton-2

Work Items
----------

* Modify PROPERTIES variable
* Modify properties_schema
* Modify handle_create()
* Implement handle_update()
* Write tests for supported Glance and user-defined metadata


Dependencies
============

Since Heat is targeting migration to Glance API v2, implementation of this
blueprint will be targeted to the particular switches of that API.  Heat code
will be modified in anticipation of the features supported by Glance v2. The
blueprint for Heat's migration to Glance v2 can be found at
`migrate-to-glance-v2
<https://blueprints.launchpad.net/heat/+spec/migrate-to-glance-v2>_`

Implemention will follow in the style of
`heat-glance-image-tag-support
<https://blueprints.launchpad.net/heat/+spec/heat-glance-image-tag-support>_`.

For more information on Glance's image metadata capabilities, please see
`Image metadata <http://docs.openstack.org/image-guide/image-metadata.html>_`.

