..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

================================================
Trigger an action in a software-config component
================================================

https://blueprints.launchpad.net/heat/+spec/software-config-trigger

OS::Heat::SoftwareComponent now allows non-lifecycle configs to be specified.
This feature will make it possible to trigger these configs and monitor their
progress and results.

Problem description
===================

OS::Heat::SoftwareComponent can specify configs to execute for stack lifecycle
actions (CREATE, DELETE etc) but it can also specify any non-lifecycle
actions (eg BACKUP, FOO, BAR). However there is currently no obvious way to
trigger these non-lifecycle actions. Once this feature is complete it should
be possible to use the heat CLI tool to do the following:

* Trigger a single config already defined in a OS::Heat::SoftwareComponent
  resource

* Monitor the progress of a triggered config

* View the resulting outputs of a triggered config

* Cancel the in-progress state of a triggered config

Proposed change
===============

Hypothetically it is already possible to trigger a single action config in a
SoftwareComponent by interacting directly with the REST API, however there is
no way to receive the results of this trigger.

Consider a SoftwareComponent which defines a config that runs on the action
BACKUP. Once stack creation is complete the following would have happened:

* Config created containing the component configs, including the BACKUP
  action config

* Derived-config created, which will add the deployment extra inputs etc
  provided by the deployment resource

* Deployment created which associates the derived-config with the nova server

Now to trigger BACKUP on a given server in the stack (optionally with some
extra input values set), REST API calls can be made to:

* Fetch the original config, modify the input values (if necessary), then
  create a derived-config. This leaves the stack-managed
  derived-config resource untouched.

* Create a swift TempURL to store the signal from the server.

* Create a trigger deployment, specifying the derived-config, the
  server, and the action BACKUP. The name of the trigger deployment is
  derived from the original deployment, plus the action name (BACKUP)

The above will all be performed by a single `heat deployment-create` command
where the user can specify all the values required to create a deployment,
including the config, server, name, action, overridden input values, etc.

Changes will be required to move some OS::Heat::SoftwareDeployment into the
deployment create call itself.

This blueprint will also depend on blueprint software-config-swift-signal
since there will need to be a signal store which is not coupled with any
stack or resources.

python-heatclient will need to be modified so that all software-config and
deployment operations can be done from the command line. New convenience
commands will also be added to trigger and monitor a single action in a
component.

This could also be an appropriate umbrella blueprint to switch to using RPC
instead of full REST calls for when config and deployment resources call
config and deployment APIs.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <steve-stevebaker>

Milestones
----------

Target Milestone for completion:
  Kilo-3


Work Items
----------

Currently python-heatclient lacks any cli commands to manage software configs
and deployments. A prerequisite for this change is cli support for
interacting with the existing config and deployment REST API, including

* Creating a software-config

* Showing a software-config

* Deleting a software-config

* Creating a software-deployment

* Showing a software-deployment

* Deleting a software-deployment

* Listing software-deployments for a given server

Once these have been implemented, new convenience commands will also be added
to trigger and monitor a single action in a component.

In heat, the following changes would be required:

* Move some OS::Heat::SoftwareDeployment into the deployment create call
  itself. Specifically, creating the derived config and the deployment could
  be combined in EngineService.create_software_deployment.

* Modify EngineService.resource_signal so that some signal calls get
  redirected to a new method EngineService.signal_software_deployment

* Functional tests to confirm the above can be used.

Dependencies
============

Not a hard dependency, but this would benefit from blueprint
software-config-progress being implemented to provide the user with feedback
that their config trigger has started.

If it is deemed inappropriate to modify EngineService.resource_signal then
some alternative external polling based signaling would be required, as
provided by blueprint software-config-swift-signal or blueprint
software-config-zaqar.