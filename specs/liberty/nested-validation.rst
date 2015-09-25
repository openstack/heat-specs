..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

===================================================
Allow validation and inspection of nested resources
===================================================

https://blueprints.launchpad.net/heat/+spec/nested-validation

Currently, there's no way to recursively validate all nested templates other
than doing a stack-create and waiting for it to fail.  Additionally, there's
no way to inspect the interfaces exposed by nested template, e.g those
accessible via parameter_defaults.  Adding more comprehensive support for
pre-create validation (e.g heat template-validate) will allow solving both
of these issues.

Problem description
===================

heat template-validate takes an optional environment argument, but it doesn't
parse the files and include a "files" map such as is consumed by create/update.

As a result, we expliclitly ignore validation of any nested stacks, even when
they are specified in the environment.  This means it's hard to validate
nested templates at all before create, other than perhaps by validating
each template individually (this part could probably be considered a bug).

However it's also problematic when a nested template exposes interfaces we
wish to interact with via parameter_defaults in the environment, e.g not
specified via the parent template via properties/parameters.  What is needed
is a way to validate the entire tree, and return a schema of the entire
tree, not only the parameters exposed by the top-level template.

For example, consider this workflow:

1. Choose parent template.
2. Choose a set of other templates and environments (or have this
   programmatically generated e.g by pulling templates from one or more known
   locations/paths)
3. Inspect that group to figure out the resource-type level
   capabilities/options. These are the first major choices a user will make,
   to determine the nested stack implementations for each type.
4. The user selects a nested stack choice for each one that has more than one
   choice (note https://review.openstack.org/#/c/196656/ discusses approaches
   for this selection to be made programmatically via the choices made in (3))
5. Reinspect given those major options for the full set of parameters such that
   the user may be prompted for mandatory and optional parameters, including
   those not exposed by the top-level parent template.
6. The user enters in values for all of the parameters and the stack gets
   created.

The topic of this spec is step 5 above, where we wish to build a schema of
parameters for the entire tree.

For a more concrete example consider this pattern (which is used commonly,
e.g in TripleO) - the parent template creates a server, then passes the ID to
some nested template which then performs some configuration steps, which are
intended to be pluggable and the interfaces are not known at the time of
writing the parent template:

.. code-block:: yaml

  resource_registry:
    OS::TripleO::ControllerExtraConfigPre: extraconfig/some_extra.yaml

  parameter_defaults:
    SomeExtraParam: "extra foo"

Here, any template may be hooked in via ControllerExtraConfigPre, and the
parent template need not know anything about the parameters exposed, other than
that a server ID may be passed in, any extra parameters are wired in at the
time of defining ControllerExtraConfigPre, e.g via parameter_defaults.

.. code-block:: yaml

  heat_template_version: 2015-04-30

  description: Configure some extra config on your server

  parameters:
    server:
      description: ID of the server to apply config to
      type: string

    # Config specific parameters, to be provided via parameter_defaults
    SomeExtraParam:
      type: string
      default: "bar"

  resources:
    ExtraServerConfig:
      type: OS::Heat::StructuredConfig
      properties:
        group: os-apply-config
         config: <some config>

    ExtraServerDeployment:
      type: OS::Heat::StructuredDeployment
      properties:
        config: {get_resource: ExtraServerConfig}
        server: {get_param: server}
        input_values:
          ImplementationSpecificStuff: {get_param: SomeExtraParam}

Here we can see the nested template consuming both the parent provided
parameter (server) and the environment provided one (SomeExtraParam).

Currently, there's no way, other than knowledge of the templates (or
inspection/parsing by non-heat tools) to know that SomeExtraParam
is a required additional parameter when choosing extraconfig/some_extra.yaml

Proposed change
===============

Firstly, we need to fix the basic syntax/structure validation part, which will
mean passing an optional "files" map to the validate API (same as for create
and update), then instead of skipping TemplateResource validation (in
service.py validate_template()) we can recurse into the child templates and
validate (similar to what happens on pre-create except we'll tolerate missing
parameters).

Then, we need to expose additional parameter information, other than what is
currently exposed (parent template parameters only), this could be done via a
new --show-nested (-n) option::

  heat template-validate -f parent.yaml -e env.yaml --show-nested

Below is a sample output when run on a group of templates with the following
properties:

* The parent template contains a single resource named ``level-1-resource``
  of type ``demo::Level1``
* The ``parent-p1`` parameter is defined by the parent template
* The ``demo::Level1`` template contains a parameter that must be specified
  by the parent and one that has a default. The latter is meant to represent
  the type of value that is specified as a ``parameter_default``.
* The ``level-1-resource`` resource contains a resource named
  ``level-2-resource`` of type ``demo::Level2``.
* Similarly, the ``demo::Level2`` template defines a non-defaulted parameter
  that must be specified by the parent and one that may optionally be
  overridden through ``parameter_defaults``.

.. code-block:: json

    {
      "Description": "parent template",
      "Parameters": {
        "parent-p1": {
          "Type": "String",
          "NoEcho": "false",
          "Description": "parent first parameter",
          "Label": "parent-p1"
        }
      },
      "NestedParameters": {
        "level-1-resource": {
          "Type": "demo::Level1",
          "Description": "level 1 nested template",
          "Parameters": {
            "level-1-p1": {
              "Type": "String",
              "NoEcho": "false",
              "Description": "set by parent; should have a Value field",
              "Value": "parent-set-value-1",
              "Label": "level-1-p1"
            },
            "level-1-p2-optional": {
              "Default": "",
              "Type": "String",
              "NoEcho": "false",
              "Description": "not set by parent",
              "Label": "level-1-p2-optional"
            }
          },
          "NestedParameters": {
            "level-2-resource": {
              "Type": "demo::Level2",
              "Description": "level 2 nested template",
              "Parameters": {
                "level-2-p2-optional": {
                  "Default": "",
                  "Type": "String",
                  "NoEcho": "false",
                  "Description": "not set by parent",
                  "Label": "level-2-p2-optional"
                },
                "level-2-p1": {
                  "Type": "String",
                  "NoEcho": "false",
                  "Description": "set by parent; should have a Value field",
                  "Value": "level-1-set-value",
                  "Label": "level-2-p1"
                }
              }
            }
          }
        }
      }
    }

Here we would return a new "NestedParameters" section, (potentially to
multiple levels of nesting), reflecting the parameters validation at each
step of recursion through child templates (or rather resource instantiations
of each child template, which may be used in more than one place with different
parameters).

The "Default" key would be included if the nested template defines a parameter
default (as usual) or if a default is set via ``parameter_defaults``.
The "Value" key would be included if a value is provided by the parent
template. Note that since parameters are optional during template-validate
calls, this could be None, e.g a Value of None indicates the parent provides
a value but it was not provided as part of the template-validate call.

This would mean that it's possible to build a schema from the returned data,
such that, for example any parameters missing both "Default" and "Value" may
be identified, as these will require operator input to provide a parameter.

The next category of parameters would be "defaulted but configurable" where
Default is present, but no Value - these values you may want to ask operators
for values other than the template default, and if constraints are specified
they will be exposed here (as choices, as with the existing Parameters section)

Note that the key naming in the returned data structure aligns with the
existing Parameters section - when we reach a v2 API it would be good to
rework both to use more native_api_style_names.

Below is the example output when the example template above is modified to
use resource groups. The only change is that the parent resource
``level-1-resource`` has been replaced by a resource group named
``level-1-groups``. The definition inside of the group is identical to
the previous example.

For brevity, the bulk of the output has been removed. The relevant point is
that each node in the group will be listed by index:

.. code-block:: json

  {
    "Description": "parent template",
    "Parameters": {
      "parent-p1": {
        "Default": "foo",
        "Type": "String",
        "NoEcho": "false",
        "Description": "parent first parameter",
        "Label": "parent-p1"
      }
    },
    "NestedParameters": {
      "level-1-groups": {
        "Type": "OS::Heat::ResourceGroup",
        "Description": "No description",
        "Parameters": {},
        "NestedParameters": {
          "0": {
            "Type": "demo::Level1",
            "Description": "level 1 nested template",
            "Parameters": {
              "level-1-p1": {},
              "level-1-p2-optional": {}
            },
            "NestedParameters": {
              "level-2-resource": {
                "Type": "demo::Level2",
                "Description": "level 2 nested template"
              }
            }
          }
        }
      }
    }
  }

Alternatives
------------

The alternative we've been working with for some time in the TripleO community
is to maintain a separate service, outside of heat, which contains logic
that is coupled to the template implementation, and knows how to wire in the
appropriate parameters, and maintains a mapping of nested template
implementations to provider resource types.

This works, but you end up with a single-purpose service which is very highly
coupled to the template implementation, which is tough from a maintainability
perpective as well as a not helping the wider heat community with their
composition and interface building needs.

Implementation
==============

There will be two stages to the implementation, first pass the files map in to
heat and make basic validation work on nested stacks via template-validate.

Then the extra data outlined above will be added via the NestedParameters key,
and finally the heatclient interfaces to consume this will be added.

It may be that additional usability features can be added to heatclient,
such as building a stub environment file containing parameter_defaults
related to the validation output (this has been discussed on the ML), but
since the requirement here is not fully defined, I won't consider it in
this spec.

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

Changes to API:

- Add support for "files" map to be passed via validate call

Changes to engine:

- Modify the template-validate path so TemplateResources are no longer skipped,
  instead recursively validate similar to the pre-create steps.
- Update template-validate code to build NestedParameter output

Changes to heatclient:

- Add --show-nested option to template-validate, which collects and populates
  the optional files map, and passes it to the API

Documentation changes:

- Update API docs to reflect the "files" optional argument


Dependencies
============

None
