..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode
..

=================================================
Custom Resource type managed by Mistral Workflows
=================================================

https://blueprints.launchpad.net/heat/+spec/mistral-new-resource-type-workflow-execution

Allow users to define custom resource types by implementing their actions as
Mistral workflows.

Problem description
===================

Heat resource types are defined by Python plugins. If users want to manage some
resource that cannot be handled by the available plugins, for example a
resource external to OpenStack, they currently need to deploy software on a
server somewhere in order to manage that resource.

If we provide a plugin where the actions are handled by Mistral workflows
defined by the user, then we can allow our users to manage custom resources
within Heat's normal operation.

Proposed change
===============

The proposed resource type would be defined in a template as follows:

.. code-block:: yaml

    custom:
      type: OS::Mistral::ExternalResource
      properties:
        actions:
          CREATE:
            workflow: {get_resource: create_workflow}
            params:
              target: create_my_custom_thing
          UPDATE:
            workflow: {get_resource: update_workflow}
          DELETE:
            workflow: {get_resource: delete_workflow}
        input:
          foo1: 123
          foo2: 456
        replace_on_change_inputs:
          - foo2
        always_update: true


Properties:

 - actions - map of actions to workflows. Allowed actions are CREATE, UPDATE,
   DELETE, SUSPEND, and RESUME. All actions are optional.
 - workflow - Workflow name or id
 - params - Params to pass to the Mistral workflow execution. The parameters
   depend on the workflow type.
 - input - values to be passed as inputs to the workflow
 - replace_on_change_inputs - a list of input names for which changes in the
   input value should cause the resource to be replaced instead of updated
   in-place. In this case we'll run the CREATE workflow on the replacement
   resource followed by the DELETE workflow on the existing one, instead of the
   UPDATE workflow.
 - always_update - if true, the UPDATE action will always run on update, even
   if there is no change in the inputs. Defaults to false.

Attributes:

 - output - Workflow execution outputs

For each Heat action, the resource plugin will start an execution of the
specified workflow (if any) and wait for it to complete. The output will be
collected and stored, in the CREATE and UPDATE actions. If the execution fails,
the resource action will also fail.

If the outputs contain a key named ``resource_id``, Heat will treat this as the
physical ID of the resource. This is the value returned by the ``get_resource``
intrinsic function.

For actions other than CREATE, the current outputs will be passed in the
Mistral environment with the key ``heat_extresource_data``. If an environment
is already specified by the user in ``params`` then this key will be merged in.
Each time a workflow completes, its outputs will be merged into the 'current'
outputs, so that not every action needs to regurgitate all of the previous
outputs to avoid losing existing data..

Alternatives
------------

It's really hard to know what a good name is. It's not clear whether this
resource belongs in the ``OS::Mistral::`` or ``OS::Heat::`` namespaces, for a
start. Decent names might include 'ExternalResource', 'CustomResource',
'WorkflowResource'.

The SoftwareComponent resource allows specifying multiple actions for each
config. The equivalent here might look something like:

.. code-block:: yaml

      properties:
        workflows:
          - actions: [CREATE]
            workflow: {get_resource: create_workflow}
          - actions: [CREATE, UPDATE]
            workflow: {get_resource: update_workflow}
          - actions: [DELETE]
            workflow: {get_resource: delete_workflow}

However, it's unclear how to correctly handle the outputs when there are
multiple workflows per action. Take the output of the first action? The last
one? Some combination? Given that it's already easy to call a workflow from
another workflow, it seems better to put this in the user's hands and require
them to specify only one workflow per action. Mistral is designed for workflows
to call each other.

The equivalent in CloudFormation, AWS::CloudFormation::CustomResource using
Lambda to manage the external resource, allows the Lambda function to determine
`when to replace the resource`_. If it returns a new resource ID then the
resource is deemed to have been replaced, and the old one is then deleted. This
would be difficult to replicate in Heat - while a resource can raise
UpdateReplace at any time during an update, there is no mechanism for
preserving the data returned by the update workflow execution and storing it in
the *new* resource. (Also, it would be strange if the replacement resource did
not run the CREATE workflow.) Therefore we have chosen to force the user to
choose upfront when to replace the resource based on changing input parameters,
even though this is significantly less flexible (although Lambda functions are
easier to write than Mistral workflows, so the flexibility would come with
significant complexity too).

In the future we could add a separate should-update-replace workflow step, to
allow the user to run a workflow that returns True to replace or False to
update in-place.

.. _when to replace the resource: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#w1ab2c19c12d105c21

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  gfidente
  therve

Milestones
----------

Target Milestone for completion:
  pike-2

Work Items
----------

- Implement the new resource type

Dependencies
============

None.
