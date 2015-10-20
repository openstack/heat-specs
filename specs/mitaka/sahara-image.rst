..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


===============================
Implement Sahara image resource
===============================

https://blueprints.launchpad.net/heat/+spec/sahara-image

Add support for Sahara image resource which will allow to register images
in sahara and add tags.

Problem description
===================

Before creating a cluster we have to register an image in the sahara image
registry and add tags. Currently we can do this using sahara CLI or UI and
then create a stack with sahara resources (node group template, cluster
template and cluster). It would be more comfortable to register/unregister
an image using the same template when a stack is created/deleted.

Proposed change
===============

Implement OS::Sahara::ImageRegistry resource:

Properties:

* image (required) - image id to register
* username (required, update allowed) - username of privileged user in the
  image
* description (optional, update allowed) - description of the image
* tags (optional, update allowed) - tags to add to the image

Usage example:

.. code-block:: yaml

  glance-image:
    type: OS::Glance::Image
    properties:
      name: sahara-icehouse-vanilla-1.2.1-ubuntu-13.10
      disk_format: qcow2
      container_format: bare
      location: http://sahara-files.mirantis.com/sahara-icehouse-vanilla-1.2.1-ubuntu-13.10.qcow2

  sahara-image:
    type: OS::Sahara::ImageRegistry
    properties:
      image: {get_resource: glance-image}
      username: ubuntu
      tags: ['vanilla', '1.2.1']

Alternatives
------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  tlashchova

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

* Add Sahara image resource
* Add required test cases

Dependencies
============

None
