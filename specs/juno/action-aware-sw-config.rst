..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Action-aware Software Configuration
===================================

https://blueprints.launchpad.net/heat/+spec/action-aware-sw-config

Heat resources have a well-defined lifecycle, handling the lifecycle actions
CREATE, DELETE, SUSPEND, RESUME and UPDATE. Software components in a Heat
template should follow the same lifecycle-awareness and allow for users to
provide configuration hooks for the aforementioned actions.


Problem description
===================

With the current design of Heat software orchestration, "software components"
defined through SoftwareConfig resources allow for only one configuration (e.g.
one script) to be specified. Typically, however, a software component has a
lifecycle that is hard to express in a single script. For example, software must
be installed (created), there should be support for suspend/resume handling, and
it should be possible to allow for deletion-logic. This is also in line with the
general Heat resource lifecycle.

To achieve the desired behavior of having all those lifecycle hooks with the
current design, one would have to define several SoftwareConfig resources along
with several SoftwareDeployment resources, each addressing one specific
lifecycle action. Alternative, one would have to design automation scripts in a
way so they can conditionally handle each lifecycle action accordingly. Both of
those options lack some intuitiveness or impose complexity on the creation of
automation scripts. By making software components action-aware like other Heat
resources, thus leveraging more of the orchestration capabilities of the Heat
engine, creation of software configuration automation and respective Heat
templates can be simplified for users.


Proposed change
===============

It is proposed to make software components (defined through SoftwareComponent
and SoftwareDeployment resources) lifecylce-action-aware by allowing users to
provide configuration scripts for one software component for all standard Heat
lifecycle actions (CREATE, DELETE, SUSPEND, RESUME, UPDATE).
Those configurations that collective belong to one software component (e.g.
Tomcat web server, MySQL database) can be defined in one place (i.e. one
*SoftwareComponent* resource) and can be associated to a server by means of one
single SoftwareDeployment resource.

The new SoftwareComponent resource will - like the SoftwareConfig resource - not
gain any new behavior, but it will also be static store of software
configuration data. Compared to SoftwareConfig, though, it will be extended to
provide several configurations corresponding to Heat lifecyle actions in one
place and following a well-defined structure so that SoftwareDeployment
resources in combination with in-instance agents can act in a lifecycle-aware
manner.


.. _software_component_resource:

New SoftwareComponent resource
------------------------------

It is proposed to implement a new resource type OS::Heat::SoftwareComponent,
which is similar to the existing SoftwareConfig resource, but has a richer
structure and semantics.
As an alternative, we could choose to extend the existing "SoftwareConfig"
resource, but the overloaded semantics could cause confusion with users.
Furthermore, extension of the existing resource could raise additional
complexity when having to maintain backwards-compatibility with existing uses of
SoftwareConfig.

The set of properties for OS::Heat::SoftwareComponent will be as follows:

.. code-block:: yaml

  # HOT representation of new SoftwareComponent resource

  sw-config:
    type: OS::Heat::SoftwareComponent
    properties:
      # per action configurations
      configs:
        - actions: [ string, ... ]
          config: string
          tool: string
        - actions: [ string, ... ]
          config: string
          tool: string
        # ...
      # inputs and outputs
      inputs: [ ... ]
      outputs: [ ... ]
      options: { ... }

The *configs* property is a list of configurations for the various lifecycle
operations of a software component. Each entry in that list defines the
following properties:

actions
  This property defines a list of resource actions when the respective config
  should be applied. Possible values in that list correspond to lifecycle
  actions of Heat's resource model (i.e. CREATE, DELETE, SUSPEND, RESUME, and
  UPDATE).
  Making this property a list of actions allows for re-using one configuration
  for multiple resource actions when desired. For example, Chef recipe for
  deploying some software (i.e. CREATE action) could also be used for handling
  updates to software configuration properties (i.e. UPDATE action).

  **Note:** One action like CREATE is only allowed to appear in the *actions*
  property of at most one config. Otherwise, the ordering of several configs
  for one lifecycle action at runtime would be unclear. This constraint will be
  validated in the *validate()* method of the SoftwareComponent resource.
  Allowing an action to appear in more than one config (probably with
  additional annotation for ordering) is something that could be done as future
  work.
config
  This property defines the actual configuration to be applied, analogous to
  the *config* property of OS::Heat::SoftwareConfig.
tool
  This property specifies the configuration tool to be used. Note that this is
  analogous to the SoftwareConfig resource's *group* property, but it has been
  suggested to use a more intuitive name here.
  Having the *tool* property for each config entry allows for mixing different
  configuration tools for one software component. For example, the deployment of
  software (i.e. CREATE) could be done using Chef or Puppet, but a simple script
  could be used for SUSPEND or RESUME.

The *inputs* and *outputs* properties will be defined global for the complete
SoftwareComponent definition instead of being provided per config hook.
Otherwise, the corresponding SoftwareDeployment resource at runtime would
potentially have different or stale attributes depending on which resource
action was last run, which would likely introduce more complexity.
Template authors will have to make sure that the defined *inputs* and *outputs*
cover the superset of inputs and outputs for all operation hooks. Typically,
the CREATE hook will require the broadest set of inputs and produce most
outputs.

The *options* property will also be defined globally for the complete
SoftwareComponent. This property is meant to provide extra options for the
respective configuration tool to be used. It is assumed that the same options
will apply to all invocations of a configuration for one SoftwareComponent, so
making this a per-config settings does not make sense.
Note that in case of multiple configuration tools being used in one
SoftwareComponent, options need to be namespaced so they can mapped to the
respective tools. For that reason, the *options* map will have to contain
sub-sections for the respective tools. For example, for Chef the *options* map
would contain a 'chef' entry the value of which is in turn a map of
Chef-specific options.

Example
~~~~~~~

The following snippet shows an example of a SoftwareComponent definition for an
application server. The SoftwareComponent defines dedicated hooks for CREATE,
UPDATE and SUSPEND operations.

.. code-block:: yaml

  appserver-config:
    type: OS::Heat::SoftwareComponent
    properties:
      # per action configurations
      configs:
        - actions: [ CREATE ]
          config: { get_file: scripts/install_appserver.sh }
          tool: script
        - actions: [ UPDATE ]
          config: { get_file: scripts/reconfigure_appserver.sh }
          tool: script
        - actions: [ SUSPEND ]
          config: { get_file: scripts/drain_sessions.sh }
          tool: script
      # inputs and outputs
      inputs:
        - name: http_port
        - name: https_port
        - name: default_con_timeout
      outputs:
        - name: admin_url
        - name: root_url


Adaptation of SoftwareDeployment resource
-----------------------------------------

The SoftwareDeployment resource (OS::Heat::SoftwareDeployment) will be adapted
to cope with the new SoftwareComponent resource, for example to provide the
contents of the *configs* property to the instance in the appropriate form.
Furthermore, the SoftwareDeployment resource's action and state (e.g. CREATE and
IN_PROGRESS) will be passed to the instance so the in-instance configuration
hook can select the right configuration to be applied (see also
:ref:`in_instance_hooks`).

The SoftwareDeployment resource creates transient configuration objects at
runtime for providing data to the in-instance tools that actually perform
software configuration. When a SoftwareComponent resource is associated to a
SoftwareDeployment resource, the complete set of configurations of the software
component (i.e. the complete *configs* property) will be stored in that
transient configuration object, and it will therefore be available to
in-instance tools.

There will be no change in SoftwareDeployment properties, but there will have to
be special handling for the *actions* property: the *actions* property will be
ignored when a SoftwareComponent resource is associated to a SoftwareDeployment.
In that case, the entries defined in the *configs* property will provide the set
of actions on which SoftwareDeployment, or in-instance tools respectively, shall
react.

Note: as an alternative to passing the complete set of configurations defined in
a SoftwareComponent, along with the SoftwareDeployment's action and state to the
instance, we could make the SoftwareDeployment resource select the right config
based on its action and state and only pass this to the instance. This could
possibly allow for using the existing in-instance hooks without change. However,
at the time of writing this spec, it was decided to implement config select in
the in-instance hook since it gives more power to the in-instance implementation
for possible future enhancements.


.. _in_instance_hooks:

Update to in-instance configuration hooks
-----------------------------------------
The in-instance hooks (55-heat-config) have to be updated to select the
appropriate configuration to be applied depending on the action and state
indicated by the associated SoftwareDeployment resources.

In case of a *SoftwareComponent* being deployed, the complete set of
configurations will be made available to in-instance hooks via Heat metadata.
In addition, SoftwareDeployment resources will add their action and state to the
metadata (e.g. CREATE and IN_PROGRESS). Based on that information, the
in-instance hook will then be able to select and apply the right configuration
at runtime.

As an alternative, we could choose to implement SoftwareDeployment in a way to
only pass that configuration to the instance (via Heat metadata) that
corresponds to its current action and state. In-instance tools could then
potentially remain without changes (see also note in previous section).


Alternatives
------------

Without any change to current implementation, the following alternatives for
providing action-specific configuration hooks for a software component would
exist:

Use of OS::Heat::StructuredConfig
  StructuredConfig allows for defining a map of configurations, i.e it would
  allow for defining the proposed structure of the *configs* property to be
  added to SoftwareConfig. However, StructuredConfig does not define a schema
  for that map and would thus allow for any free-form data which would make it
  much harder to enforce well-defined handling.
  In addition, this would change the semantics of the map structure in
  StructuredConfig and thus it would be abuse of this resource.
Use of several SoftwareConfigs and SoftwareDeployments:
  As already outlined in the problem description, with the current design it
  would be possible to define separate SoftwareConfigs and SoftwareDeployments,
  each corresponding to one lifecycle resource action. However, this makes
  templates much more verbose by having many resources for representing one
  software component, and the overall structure does not align with the general
  structure of all other Heat resources.
Use of scripts that conditionally handle actions
  It would be possible to provide scripts that get invoked for all of a
  resource's lifecycle actions. Those scripts would have to include a lot of
  conditional logic, which would make them very complicated.


Potential follow-up work
------------------------
The current specification and implementation will only cover Heat's basic
lifecycle operations CREATE, DELETE, SUSPEND, RESUME and UPDATE. It is
recognized that special handling might make sense for scenarios where servers
are being quiesced for an upgrade, or where they need to be evacuated for a
scaling operation. In addition, users might want to define complete custom
actions (see also :ref:`software_component_resource`). Handling of those actions
are out of scope for now, but can be enabled by follow-up work on-top of the
implementation of this specification. For example, an additional property
*extended_action* could be added to SoftwareDeployment which could be set to
the extended actions mentioned above. When passing this additional property to
in-instance hooks, the hooks could then select and apply the respective config
for the specified extended action.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Thomas Spatzier


Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

* Create new OS::Heat::SoftwareComponent resource
* Adapt OS::Heat::SoftwareDeployment for new SoftwareComponent
* Adapt in-instance hook for selecting right configuration to be applied


Dependencies
============

None
