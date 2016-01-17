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

=============================
 Stack lifecycle plugpoint
=============================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/stack-lifecycle-plugpoint

A cloud provider may have a need for custom code to examine stack requests
prior to performing the operations to create or update a stack.
Some providers may also need code to run after operations on
a stack complete. A mechanism is proposed whereby providers may easily add
pre-operation calls from heat to their own code, which is called prior to
performing the stack work, and post-operation calls, which are made after
a stack operation completes or fails.


Problem description
===================

There are at least two primary use cases.
(1) Enabling holistic (whole-pattern) scheduling of the virtual resources
in a template instance (stack) prior to creating or deleting them.
This would usually include making decisions about where to host virtual
resources in the physical infrastructure to satisfy policy requirements.
It would also cover failing a stack create or update if the policies
included with the stack create or update were not satisfiable, or other
cloud provider policies being checked were not satisfiable.
As an example, an application owner requires that VMs and volumes
attached to them are deployed on the same rack. As another example,
a cloud provider may want to enforce consultation with a license server
before deploying an application. As another example, an application owner
may require that their VMs be spread across a given number of
racks.
(2) Enabling checking of policies not related to virtual resource scheduling,
with stack create or update failure if the policies would not be satisfied.
As an example, a cloud provider may want to verify that compute resources
for certain types of applications are deployed with certain security groups.
As another example, a cloud provider may want to be warned when patterns
with > 100 VMs are deployed.

Proposed change
===============

An ordered registry of python classes which implement pre-operation and/or
post-operation methods is required. This would be done through stevedore,
with some addition to force a full (or partial) ordering on the classes.
Pre and post operation methods should not modify the parameter stack(s).
Any modifications would be considered to be a bug.
A possible exception would be to allow status changes
to the stack, to facilitate error handling.
[The no-modifications rule could be enforced, e.g. by passing deep copies to
the plugins but this might incur an unacceptable
performance cost.] Both pre-operation and
post-operation methods can both indicate failure, which would be treated like
any other stack failure. On failure of a pre-operation call, when more than
one plugin
is registered, the post-op methods would be called for all the classes already
processed, to indicate to each plugin that any decisions that
it made with respect to the stack should be un-made.

All stack actions would need calls to either pre or post operations, or both.
This includes at least create, update, delete, abandon, and adopt. In a basic
design, modifications to the Stack class in parser.py are sufficient for adding
the call to the pre-operation and post-operation methods found via the
lifecycle plugin registry. The post-operation calls would need to be called in
both the normal paths and all error paths.

Alternatives
------------

No other approach was identified that would allow the operator (heat provider)
to extend heat with this functionality for all stack deployments.

https://blueprints.launchpad.net/heat/+spec/lifecycle-callbacks describes
an approach where heat users can optionally specify callbacks for in templates
for stack and resource events.
It does not provide the ubiquitous callbacks (for all stacks) that would be
needed by the use cases described above, unless the heat provider tightly
controls the templates that users can use.

Implementation
==============


A patch comprising a full implementation of the blueprint
(https://review.openstack.org/#/c/89363/) is already being
reviewed, under the old pre-spec process.

Assignee(s)
-----------

Primary assignee:
  William C. Arnold (barnold-8)

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

Implementation: https://review.openstack.org/#/c/89363/



Dependencies
============

No dependencies
