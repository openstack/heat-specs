..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

================================================
Signaling SoftwareDeployment resources via Swift
================================================

https://blueprints.launchpad.net/heat/+spec/software-config-swift-signal

Currently the only option for signaling a deployment resource requires making
an authenticated API request to heat. A SoftwareDeployment resource
signal_transport: TEMP_URL_POLL will allow unauthenticated signaling using a
similar approach to OS::Heat::SwiftSignal.

Problem description
===================

OS::Heat::SoftwareDeployment signal_transport options currently both require
resource scoped credentials and network connectivity from the server to a
heat API to work.


Proposed change
===============

Like OS::Heat::SwiftSignal, signal_transport:TEMP_URL_POLL would create a
long-lived swift TempURL which is polled by heat until the object contains
the expected data from the nova server performing the configuration
deployment. Initially, "long-lived" will mean expiring in year 2038.

Implementing a signal_transport:TEMP_URL_POLL would have the following
benefits:

* Each OS::Heat::SoftwareDeployment resource would not need to create a
  stack user

* Making swift objects accessible from nova servers is more likely to be
  provided for by the cloud operator, compared to access to keystone and heat
  APIs.

Also, heat.conf default_software_config_transport option will be added so that
operators can choose the most appropriate transport for their cloud. Choosing
the default will depend on whether the cloud supports keystone v3, swift and
the cloudformation endpoint.

Alternatives
------------

Blueprint software-config-zaqar will implement signal_transport:ZAQAR_MESSAGE
which would be the preference for clouds which offer a zaqar endpoint. Since
Swift is much more widely deployed than Zaqar then ZAQAR_MESSAGE should be
recommended first, followed by TEMP_URL_POLL.

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

* Implement TempURL creation and polling in SoftwareDeployment

* Implement TempURL POSTing in heat-templates 55-heat-config (may not be
  required if interface is identical to CFN_SIGNAL)

* Document implications for using TEMP_URL_POLL and AUTO in the
  software-deployment section of the hot-guide.

Dependencies
============

No dependencies on new libraries or existing blueprints.
