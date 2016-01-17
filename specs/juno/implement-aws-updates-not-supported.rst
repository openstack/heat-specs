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

=======================================================
Implement equivalent to AWS "Updates are not supported"
=======================================================

As Heat tries to maintain compatibility of its AWS resources,
a user can expect that a template using Heat's AWS compatible resources
will work the same both on Heat and on AWS.
Currently though we are missing a specific behavior of some AWS resources
on stack update - a property of resource might not support any updates,
including UpdateReplace (that is currently our default update behavior).

https://blueprints.launchpad.net/heat/+spec/implement-aws-updates-not-supported

Problem description
===================

AWS CloudFormation
------------------

AWS CloudFormation has a distinction between "Update requires: Replacement"
and "Update requires: Updates are not supported" for a property of a resource.
In latter case, an attempt to update this property during a stack update
will result in an error putting resource in UPDATE_FAILED state.

Example
~~~~~~~

The ``AWS::EC2::Volume`` resource has all properties marked as
"Update requires: Updates are not supported" in AWS docs [1]_.
This is the relevant part of AWS event when trying to increase the volume size
from 10 to 11 using ``update-stack`` command::

    {
     "ResourceStatus": "UPDATE_FAILED",
     "ResourceType": "AWS::EC2::Volume",
     "ResourceStatusReason":
        "Update to resource type AWS::EC2::Volume is not supported.",
     "ResourceProperties":
        "{\"AvailabilityZone\":\"us-west-2a\",\"Size\":\"11\"}"
    }

Heat
----

In Heat we currently have default update behavior as ``UpdateReplace``.
Any updateable properties must be explicitly declared as such
and handled in ``handle_update`` method of a resource.
We have no clear way of completely denying any update to a resource
(including replacing it with new resource).
Thus if one e.g. follows the same scenario as in Example_ above,
the stack update succeeds having replaced the volume.

From currently implemented AWS compatible resources the following are affected:

* ``AWS::EC2::Volume`` - Updates are not supported [1]_
* ``AWS::EC2::VolumeAttachment`` - Updates are not supported [2]_
* ``AWS::CloudFormation::WaitCondition`` - Updates are not supported [3]_
* ``AWS::CloudFormation::Stack`` - Updates are not supported for
  ``TimeoutInMinutes`` property [4]_

.. [1] http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html
.. [2] http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volumeattachment.html
.. [3] http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
.. [4] http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html

Proposed change
===============

- add a property schema attribute ``update_replace_allowed`` with default value
  ``True``
- modify ``Resource.update_template_diff_properties`` method to raise
  ``NotSupported`` error (a check similar to check for
  ``update_allowed``)

The properties schema of a resource then can specify
``update_replace_allowed=False`` which would lead to resource update
failure on any attempt to update such property.

Alternatives
------------

As an alternative we might mark all the properties of the AWS resource
in question as ``update_allowed`` and raise the same error in resource's
``handle_update``. This though would make the ``update_allowed`` effectively
a no-op, confusing users and documentation.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Pavlo Shchelokovskyy (pshchelo)

Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------

* add ``update_replace_allowed`` property attribute
* modify the default resource update logic
* amend docs generation to display the status of this attribute for a property
  (probably only if it is ``False``)
* mark corresponding properties of AWS compatible resources as
  ``update_replace_allowed = False``

Dependencies
============

None
