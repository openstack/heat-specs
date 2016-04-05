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

=========================================================
Resource plugins for Networking Service Function Chaining
=========================================================

https://blueprints.launchpad.net/heat/+spec/sfc-heat

Adds resources plugin for Networking Service Function Chaining.

Problem description
===================

OpenStack neutron suppports Service Function Chaining (sfc) as an official
sub-project and more details are available at
http://docs.openstack.org/developer/networking-sfc/ . Heat does not provide
resource plugins for Networking Service Function Chaining and this blueprint
is created to provide required plug-ins.

The proposed change is to introduce a Service Function Chaining by grouping
order of service function VM's neutron ports to form service chain and steer
classified user traffic into chain based on service treatment required.

Proposed change
===============

Add following resource plugins under resources/openstack/neutron/ and also add
port_pair, port_pair_group, flow_classifier neutron constraints for resource
validation.

* OS::Neutron::PortPair:

  * name
      - type: string
      - update_allowed: true

  * description
      - type: string
      - required: false
      - update_allowed: true

  * ingress
      - type: string
      - required: true
      - constraints: Custom Constrain 'neutron.port'

  * egress
      - type: string
      - required: true
      - constraints: Custom Constrain 'neutron.port'

  * service_function_parameters
      - type: map
      - required: false
      - default: {'correlation': None}

* OS::Neutron::PortPairGroup:

  * name
      - type: string
      - update_allowed: true

  * description
      - type: string
      - required: false
      - update_allowed: true

  * port_pairs
      - type: list
      - default: []
      - required: true
      - update_allowed: true
      - constraints: Custom Constrain 'neutron.port_pair'

* OS::Neutron::PortChain:

  * name
      - type: string
      - update_allowed: true

  * description
      - type: string
      - required: false
      - update_allowed: true

  * port_pair_groups
      - type: list
      - default: []
      - required: true
      - constraints: Custom Constrain 'neutron.port_pair_group'

  * flow_classifiers
      - type: list
      - default: []
      - required: false
      - update_allowed: true
      - constraints: Custom Constrain 'neutron.flow_classifier'

  * chain_parameters
      - type: map
      - required: false
      - default: {correlation: mpls}

* OS::Neutron::FlowClassifier:

  * name
      - type: string
      - update_allowed: true

  * description
      - type: string
      - required: false
      - update_allowed: true

  * protocol
      - type: string
      - required: false
      - allowed_values: [tcp, udp, icmp, any]

  * ethertype
      - type: string
      - required: false
      - allowed_values: [IPv4, IPv6]
      - default : Ipv4

  * source_ip_prefix
      - type: string
      - required: false
      - default: [correlation=mpls]
      - constraints: Custom Constrain 'net_cidr'

  * destination_ip_prefix
      - type: string
      - required: false
      - default: [correlation=mpls]
      - constraints: Custom Constrain 'net_cidr'

  * source_port_range_min
      - type: string
      - required: false
      - constraints.Range: (1, 65535)

  * source_port_range_max
      - type: string
      - required: false
      - constraints.Range: (1, 65535)

  * destination_port_range_min
      - type: string
      - required: false
      - constraints.Range: (1, 65535)

  * destination_port_range_max
      - type: string
      - required: false
      - constraints.Range: (1, 65535)

  * logical_source_port
      - type: string
      - required: true
      - constraints: Custom Constrain 'neutron.port'

  * logical_destination_port
      - type: string
      - required: false
      - constraints: Custom Constrain 'neutron.port'

  * l7_parameters
      - type: map
      - required: false

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Mohankumar (nmohankumar1011@gmail.com)

Milestones
----------

  newton-1

Work Items
----------

* Add resources related
* Add required custom constraints
* Add related tests
* Add sample template in heat-templates

Dependencies
============

None

