..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

==========================
 Uniform Resource Signals
==========================

https://blueprints.launchpad.net/heat/+spec/uniform-resource-signals

This spec covers the implementation of a uniform signaling framework for
heat resources.

Problem description
===================

The standard way to signal a resource is to do it through a request to
heat-api. This works well for user generated signals, but it is often the case
that signals are not generated directly by the user, but instead are triggered
by a resource or a service when certain conditions are met. The difficulty in
triggering these internal signals is that the user credentials are not
available, so heat resources implement a variety of mechanisms to make signals
work in this context.

For example, the ``OS::Heat::ScalingPolicy`` resource exposes a ``alarm_url``
attribute that is a EC2 signed URL, so the heat-api-cfn compatibility service
must be available for these signals to work. The
``OS::Heat::WaitConditionHandle`` resource, on the other side, exposes a proper
endpoint to heat-api and a token to authenticate against it, but that only
allows signals to be sent before the token expires. Unfortunately there is no
way to renew the token, so these resources cannot be used for long tasks. Other
heat resources use swift temp URLs as signals, and yet some others expose a
more traditional set of heat-owned keystone credentials that can be used to
obtain a token to authenticate against heat-api.

Out of all these authentication methods, the only one that is implemented in
a base class accessible to all resources is EC2 signed URLs, the ones that are
based on a heat-api-cfn endpoint. The others are implemented as "one-offs" by
individual resources, making them hard to implement across resources without
code duplication.

Proposed change
===============

The heat-engine service includes a ``SignalResponder`` base class, from which
resources that can be signaled can inherit. To make the different types of
signals available to all resources, their implementations will be moved to this
class, which already contains the support for EC2 signed URLs.

With support for using all the different types of signals implemented in
``SignalResponder``, resources will be able to offer different choices of
signals, without having to deal with the particulars of each implementation.

Resources will have the option to expose a single signal type, or else
implement a ``signal_transport`` property that gives the operator the option
to select the signal type.

The credentials necessary to trigger a signal will be exposed in the resource
as an attribute called ``signal``, of type map. The items included in the map
will depend on the selected signal type.

The following signal types will be supported:

- ``CFN_SIGNAL``: The currently available EC2 signed URL signals. The signals
  are triggered by sending a request to a URL. The request method and the URL
  are given in the ``signal`` attribute. The URL is based on the heat-api-cfn
  service.
- ``TEMP_URL_SIGNAL``: Signals based on a swift temp URL. The signals are
  triggered by sending a request to a URL. The request method and the URL are
  given in the ``signal`` attribute. The URL is based on the swift service.
- ``HEAT_SIGNAL``: Signals based on the standard heat-api signal endpoint. The
  process to trigger this signal involves requesting a keystone token, then
  sending the signal request to heat-api with this token. The keystone
  credentials necessary to obtain the token are given in the ``signal``
  attribute. Note that these credentials are not the user's, but those of a
  temporary user created by heat.

Alternatives
------------

Implement a webhook solution similar to EC2 signed URLs based on a heat-api
endpoint. This is a less flexible approach, and it has the drawback that the
authentication tokens are embedded in URLs, which are typically written to
logfiles. The nice thing about the proposed solution is that nothing prevents
a webhook signal to be added to the list of signal options in the future.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  miguelgrinberg

Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

- Refactor EC2 signed URL support in ``SignalResponder`` class to allow other
  signal types to be defined.
- Implement heat-api signals in the ``SignalResponder`` class.
- Implement swift temp URL signals in the ``SignalResponder`` class.
- Add support for all the signal types in wait conditions.
- Add support for all the signal types in the scaling policy resource.
- Base signals in SoftwareDeployment on the ``SignalResponder`` class.
- Deprecate current signals in wait condition and scaling policy resources.
- Deprecate the ``default_deployment_signal_transport`` configuration item and
  replace it with one that is generic for all resources, such as
  ``default_signal_transport``.
- Documentation for the various affected resources.
- Unit tests for the various affected resources.

Dependencies
============

None
