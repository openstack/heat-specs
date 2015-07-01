..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

=====================================
"None" resource which does.. nothing!
=====================================

https://blueprints.launchpad.net/heat/+spec/noop-resource

Add a "None" resource, intended to simplify mapping resource_registry
entries to an implemention which always passes, but does nothing.

Problem description
===================

Currently, in a large tree of composable nested templates, controlled by
a number of rigidly defined parent templates, there is often the need
to provide optional interfaces where extra logic may be linked in.

Simplified example derived from TripleO (this pattern is repeated in several
places):


.. code-block:: yaml

  resource_registry:
    OS::TripleO::Controller:  foo/controller.yaml
    OS::TripleO::ControllerExtraConfig: noop.yaml

Here we have a nested template which creates a "controller" node, and does
some standard configuration.  Then, in some circumstances, we want to hook in
some extra configuration steps, or provide an interface which enables that.

.. code-block:: yaml

  resources:
    controller:
      type: OS::TripleO::Controller
      properties:
        aproperty: 123

    extra_config:
      type: OS::TripleO::ControllerExtraConfig
      properties:
        server: {get_resource: controller}

The ExtraConfig "noop.yaml" implementation is just an empty template which
takes the "server" parameter.

It would be nice to avoid having these "noop" templates duplicated, when
all they do is duplicate the interface expected for a "real" implementation,
you end up with multiple noop.yaml files with different parameters/outputs
which is inconvenient and error prone.


Proposed change
===============

Add an OS::Heat::None resource, which replaces the noop.yaml

.. code-block:: yaml

  resource_registry:
    OS::TripleO::Controller:  foo/controller.yaml
    OS::TripleO::ControllerExtraConfig: OS::Heat::None


This resource will accept any properties, and return any attribute (as None).


Alternatives
------------

The alternative is for template authors wishing to provide interfaces for
optional additional functionality to keep maintaining multiple templates
which actually do nothing, such as is happening in TripleO at the moment.

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  shardy

Milestones
----------

Target Milestone for completion:
  liberty-2

Work Items
----------

Changes to engine:
 - Implement noop resource and tests.

Documentation changes:
 - Ensure docstrings are present in code so template guide is updated.


Dependencies
============

None
