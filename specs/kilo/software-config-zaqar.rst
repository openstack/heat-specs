..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

====================================================
Use Zaqar for software-config metadata and signaling
====================================================

https://blueprints.launchpad.net/heat/+spec/software-config-zaqar

Zaqar provides a simple messaging service which allows heat and orchestrated
services to efficiently communicate with each other, which make it ideal for
software-config metadata distribution and signaling

Problem description
===================

There are a number of areas where having a messaging service like Zaqar
available can benefit Heat. Two of these are:

* Propagating server configuration metadata from heat to the servers

* Signaling from servers to heat that a software configuration event has
  occurred, with associated data.

Like OS::Nova::Server software_config_transport:POLL_TEMP_URL this will stop
servers from polling heat directly for metadata delivery which will improve
heat scalability.

Proposed change
===============

For OS::Nova::Server software_config_transport:ZAQAR_MESSAGE create a queue
dedicated to publishing metadata changes from heat to one server.
os-collect-config will need a collector which consumes messages from this
queue.

For OS::Heat::SoftwareDeployment signal_transport:ZAQAR_MESSAGE create a queue
dedicated to one server signalling configuration results to one deployment
resource. heat-templates 55-heat-config will need to be modified to depend on
python-zaqarclient and push to the queue if the required deploy input values
indicate that a queue is configured.

Just like signal_transport:HEAT_SIGNAL and
software_config_transport:POLL_SERVER_HEAT there will be a stack users
created for the deployment and server resources and the credentials for those
users will be given to the server. If and when Zaqar allows reading and
writing messages to signed webhooks then we can consider switching to this so
that it is not necessary to create the stack users.

signal_transport:AUTO will be modified so that ZAQAR_MESSAGE is the preferred
method if there is a configured messaging endpoint.

Implementation
==============

Assignee(s)
-----------

This blueprint currently has no engineer assigned to it

Primary assignee:
  <None>

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

* Implement OS::Nova::Server software_config_transport:ZAQAR_MESSAGE

* Implement OS::Heat::SoftwareDeployment signal_transport:ZAQAR_MESSAGE

* Write a Zaqar collector for os-collect-config

* Modify software-config os-refresh-config hook to use zaqar to push
  deployment signal data


Dependencies
============

python-zaqarclient will be added to heat/requirements.txt (this is already a
requirement for the zaqar contrib resource)

python-zaqarclient will become a requirement in os-collect-config and the
heat-templates heat-config element.

This could be done after blueprint software-config-trigger since that includes
some refactoring which includes moving signal_transport logic from the
resource to the deployments REST API.