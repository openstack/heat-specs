..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..
 This template should be in ReSTructured text. The filename in the git
 repository should match the launchpad URL, for example a URL of
 https://blueprints.launchpad.net/heat/+spec/awesome-thing should be named
 awesome-thing.rst .  Please do not delete any of the sections in this
 template.  If you have nothing to say for a whole section, just write: None
 For help with syntax, see http://sphinx-doc.org/rest.html
 To test out your formatting, see http://www.tele3.cz/jbar/rest/rest.html

===============================
Add Support for Resource Chains
===============================

Problem description
===================

The resource registry enables template extension and customization through
the ability to map a particular template/implementation to a resource type
name. TripleO uses this pattern extensively to provide integration points
at various steps in the stack deployment that can be used to add 3rd party
integrations, such as service and driver configuration.

The problem is, only one template can be specified for each of these hooks.
This spec is attempting to alleviate that by introducing a new type that
will aggregate one or more templates into a nested stack.

Proposed change
===============

The proposed change is to introduce a ``ResourceChain`` type, similar in
behavior to the existing ``ResourceGroup``. For example:

.. code-block:: yaml

 resources:
   MyChainResource:
     type: OS::Heat::ResourceChain
     properties:
       resources: <list>  # resource types to add to the chain's nested stack
       concurrent: <boolean>  # optional; default is false
       resource_properties:
         # properties to pass each template in the chain

Internally, Heat will create a nested stack comprised of each template
specified in the chain's configuration.

By default, each resource will be treated as having a dependency on the
resource before it in the list. If the ``concurrent`` property is set to
true, no dependencies between the created resources will be established.

A failure in a resource creation will abort the creation of the remaining
resources in the chain (and obviously flag the chain resource as failed).
This will allow users to control the order in which the resources in the
chain will be created. If it is set to false, the resources in the chain
will be created concurrently.

The ``resource_properties`` parameter is similar to the ``properties``
section of the ``resource_def`` used in a resource group and will be
passed to each of the resources in the chain's stack.

Resources in the chain may be accessed by index, where the index corresponds
to the template's location in the ``resources`` property.

The primary drawback is that it moves the template selection from the
resource registry out to the parameters section. There is the potential to
confuse users attempting to extend a template if some of the substitutions
are done in the registry while others are done through parameters. This will
also complicate the capabilities detection since we'll have to take into
account templates specified not only in the registry, but through a parameter
as well.

To apply this to the TripleO use cases, below is an example of how resource
chains may be used to configure which resources are created at a particular
step in the deployment::

  ControllerDeploymentSteps:
    type: json
    default:
      step1: [controller/loadbalancer.yaml]
      step2: [controller/db.yaml, controller/rabbit.yaml]
      step3: [controller/keystone.yaml, controller/glance-api.yaml ...]

  [snip]

  DeploymentStep1:
    type: OS::Heat::ResourceChain
      properties:
        resources: {get_param: [ControllerDeploymentSteps, step1]}
        resource_properties:
          servers: {get_param: servers}

  DeploymentStep2:
    type: OS::Heat::ResourceChain
      properties:
        resources: {get_param: [ControllerDeploymentSteps, step2]}
        resource_properties:
          servers: {get_param: servers}

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  jdob

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

* Add a resource plugin for ResourceChain
* Add the corresponding functional tests

Dependencies
============

None
