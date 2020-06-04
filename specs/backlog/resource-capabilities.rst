..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

===============================================================
Add Template "Capabilities" Annotation/Resolution/Introspection
===============================================================

https://blueprints.launchpad.net/heat/+spec/resource-capabilities

Also related to https://blueprints.launchpad.net/heat/+spec/interface-types

Add an optional annotation to HOT which enables a template author to
define that a template implements/provides particular capabilities.

Problem description
===================

Currently, the environment resource_registry provides an extremely flexible
but completely unconstrained interface for mapping type aliases to
implementation.

This makes it difficult for those wishing to use the resource_registry for
composition, in particular if you wish to offer users the choice to pick
a particular implementation of a provider resource template.

For example, consider this workflow:

1. Choose parent template.

2. Choose a set of other templates and environments (or have this
   programmatically generated, for instance by pulling templates from one or
   more known locations/paths).

3. Inspect that group to figure out the resource-type level
   capabilities/options. These are the first major choices a user will make to
   determine the nested stack implementations for each type.

4. The user selects a nested stack choice for each one that has more than one
   choice.

5. Reinspect given those major options for the full set of parameters such
   that the user may be prompted for mandatory and optional parameters,
   including those not exposed by the top-level parent template.

6. The user enters in values for all of the parameters and the stack gets
   created.

The topic of this spec is steps 3 and 4 above.
https://review.openstack.org/#/c/197199 discusses step 5. The other steps
are already possible.

The discussion below focuses on the TripleO use case, since that is what is
motivating this work (TripleO makes very heavy use of template composition via
the ``resource_registry``). However, the feature should be generally useful to
anyone wishing to use the ``resource_registry`` to build a complex environment
from a tree of interrelated templates via the ``resource_registry``.

Here's an example of the ``resource_registry`` mapping used for TripleO
controller node implementation:

.. code-block:: yaml

  resource_registry:
    OS::TripleO::Controller: puppet/controller-puppet.yaml
    OS::TripleO::Controller::Net::SoftwareConfig: net-config-bridge.yaml
    OS::TripleO::ControllerPostDeployment: puppet/controller-post-puppet.yaml
    OS::TripleO::ControllerConfig: puppet/controller-config.yaml
    OS::TripleO::Controller::Ports::ExternalPort: network/ports/noop.yaml
    OS::TripleO::Controller::Ports::InternalApiPort: network/ports/noop.yaml
    OS::TripleO::Controller::Ports::StoragePort: network/ports/noop.yaml
    OS::TripleO::Controller::Ports::StorageMgmtPort: network/ports/noop.yaml
    OS::TripleO::Controller::Ports::TenantPort: network/ports/noop.yaml
    OS::TripleO::Controller::CinderBackend: extraconfig/controller/noop.yaml

We can see that there are a large number of choices (and this is only a tiny
subset of the full environment), with no way for a UI to determine what
are valid choices for any of the mappings.  It would be beneficial to
describe directly in the template what valid implementations are, such that
they may be discovered by UI/CLI tools and constrained at validation time.

Taking the above as a worked example, there are multiple choices to be made:

* Configuration Tool type (all ``puppet/*.yaml`` resource)
* NIC configuration (physical network, e.g bridged, bonded, etc)
* Port assignement (overlay network, where ``ports/noop.yaml`` assigns all
  ports to a common network)
* Choice of (potentially multiple CinderBackend implementations)

For simplicity, the examples below will consider only the choice between puppet
and some other implementation.


Proposed change
===============

The proposed change covers three areas:

* :ref:`capabilities-annotations` - How to convey the relationship between a
  resource type and templates that may potentially fufill the type.
* :ref:`capabilities-resolution` - How Heat can use user settings on the stack
  to choose the most applicable template to fulfill a resource type from a
  list of options.
* :ref:`capabilities-introspection` - How a UI can programmatically use the
  annotations to present the user with an interface in which to select an
  option for each eligible resource type.

The remainder of this change is broken up into those three sections. It should
be noted that all three are not necessary for a minimal viable feature. It is
possible that the implementation for mitaka only covers, for example, the
annotations and introspection APIs necessary for the user to understand the
"schema" (for lack of a better word) around selecting template implementations
for a stack.

.. _capabilities-annotations:

Annotation
----------

Add an optional template annotation, inspired by the TOSCA
"substitution_mappings" interface [1]_, which allows an optional new block in
HOT templates where template authors may declare that a template provides a
particular set of capabilities.

There are two slightly different uses of the capabilities annotation being
proposed.

Tag-Based
^^^^^^^^^

For example, there may be multiple valid implementations of
``OS::TripleO::Controller``. For the Puppet-based implementation, the
capabilities annotation on the template will indicate it:

.. code-block:: yaml

  heat_template_version: 2015-10-15

  capabilities:
     deployment: puppet

The syntax used here is similar to that defined in the TOSCA spec but the names
have been adjusted to better match existing HOT conventions. The capabilities
section will not be strictly validated; it will be possible to add extra
key/value pairs that are not specified in the environment, such that templates
may be portable.

.. _capabilities-annotation-type:

Type-Based
^^^^^^^^^^

It also may be possible to use these annotations for client-side discovery
of the list of valid templates to be passed via the ``resource_registry`` by
specifically referencing the name of the resource type the template may be
used as a mapping for:

.. code-block:: yaml

 heat_template_version: 2015-10-15

 capabilities:
    resource_type: OS::TripleO::Controller

This should support a list as TripleO has already seen an example of templates
that can be used as either the computer or controller hooks:

.. code-block:: yaml

 heat_template_version: 2015-10-15

 capabilities:
    resource_type: [OS::TripleO::ControllerPostDeployment,
                    OS::TripleO::ComputePostDeployment]

.. _capabilities-resolution:

Resolution
----------

In the environment, an optional new "requires" section will be
added and support for ``resource_registry`` keys containing a list of
multiple implementations. Heat will then be able to resolve the
implementation that should be chosen by matching the environment
requires to the list of possible templates with (hopefully matching)
capabilities. A validation error will be thrown should either zero or multiple
implementations be found.

For example, expanding on the examples from the previous section, take the
following environment file:

.. code-block:: yaml

 requires:
    deployment: puppet

 resource_registry:
    OS::TripleO::Controller: [puppet/controller.yaml, docker/controller.yaml]

Adding annotations to the two referenced templates, we have:

.. _capabilities-ex-puppet:

``puppet/controller.yaml``

.. code-block:: yaml

 heat_template_version: 2015-10-15

 capabilities:
    deployment: puppet

.. _capabilities-ex-docker:

``docker/controller.yaml``

.. code-block:: yaml

 heat_template_version: 2015-10-15

 capabilities:
    deployment: docker

Putting these three files together, Heat would use the ``capabilities`` section
to determine which of the two ``controller.yaml`` files to use.

.. _capabilities-introspection:

Introspection
-------------

The functionality described in the :ref:`capabilities-annotations` section
provides enough information for Heat to provide a series of introspection
queries to facilitate the user experience.

Specific Type Query
^^^^^^^^^^^^^^^^^^^

Given a specific resource type name, the Heat API should be able to return a
list templates that claim to support that type (note: this is contingent on
using the :ref:`capabilities-annotation-type` annotation style described
above).

A potential example of the output of such a query through the Heat client
is below:

.. code-block:: bash

  $ heat capabilities-find -r -c resource_type=OS::TripleO::Controller ./*
  puppet/controller.yaml
  docker/controller.yaml

This would recurse from the current directory inspecting the capabilities in
each template, returning a list of those which match the capabilities required
(with the possibility of passing multiple ``-c`` options if necessary).
This makes multiple implementations discoverable on the client side.

Capabilities Summary
^^^^^^^^^^^^^^^^^^^^

There is also a need to have Heat analyze a series of templates and
environments, returning a list of all capabilities that can be specified:

For example, given the :ref:`Puppet <capabilities-ex-puppet>` and
:ref:`Docker <capabilities-ex-docker>` example templates above:

.. code-block:: bash

  $ heat template-capabilities -f puppet/controller.yaml \
                               -f docker/controller.yaml

Which would return:

.. code-block::

  {
    'deployment': ['puppet', 'docker']
  }

A similar version of the call exists if the
:ref:`capabilities-annotation-type` annotation is used:

.. code-block::

  {
    'OS::TripleO::Controller': ['puppet/controller.yaml',
                                'docker/controller.yaml']
  }

The operator or UI then knows that these are the options which may be
resolved in order for the stack to be created.  Note this is related to
but not the same as the spec posted related to recursive validation [2]_,
which is about exposing the parameters required for stack create,
not the options related to a valid composition.

.. note:: API v. Client-side

  The original iteration of this spec spoke in terms of having the Heat client
  walk the template tree and perform the introspections described. It has since
  been changed to refer to the Heat API, moving the logic server-side and
  allowing non-Python clients access to this functionality.

.. rubric:: References
.. [1] http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csd03/TOSCA-Simple-Profile-YAML-v1.0-csd03.html#_Toc419746122
.. [2] https://review.openstack.org/#/c/197199

Alternatives
------------

The main alternative discussed (see previous revision of this patch) was
adding constraints to the ``resource_registry``, such that valid mappings may
be defined inside the environment.  This idea was rejected because of the
desire for a more discoverable interface (e.g look for valid implementations
vs a rigidly defined list of constraints).

A subsequent proposal was also rejected, which focussed on only matching
a ``resource_type`` annotation in the templates, it was suggested that this
was insufficiently granular and not flexible enough.


Implementation
==============

The implementation will require adding the new capabilities
annotation to the Mitaka HOT version, this will be optional and if
it is omitted the existing behavior will be maintained.

Then support will be added to the environment to enable lists to be
passed via the ``resource_registry``, and resolved via a new requires
section.

Assignee(s)
-----------
Primary assignee(s):

* shardy
* jdob

Milestones
----------

Target Milestone for completion:
  mitaka-2

Work Items
----------

Changes to Engine
^^^^^^^^^^^^^^^^^

* Update HOT to support optional new capabilities annotation
* Update environment code to allow lists for resource_registry
* Update environment to process capabilities section to filter lists

Changes to heatclient
^^^^^^^^^^^^^^^^^^^^^

* Add support to python-heatclient for parsing a tree of templates, returning
  a list of valid templates for a specified capability
* Add support for passing files/environment to get required capabilities

Documentation Changes
^^^^^^^^^^^^^^^^^^^^^

* Document new interfaces in template guide docs/HOT spec.


Dependencies
============

None
