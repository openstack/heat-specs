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

===========================
Support for the LBaaS V2
===========================


https://blueprints.launchpad.net/heat/+spec/lbaasv2-suport

Currently there is no support for the LBaaS V2 resources in the heat.
Add a new namespace called OS::LBaaS::* for all of the LBaaS V2 resources

Problem description
===================

There are new LBaaS V2 api in Liberty, which are needed to be supported by
heat. Since there is already LBaaS V1 api support in heat in the name space
OS::Neutron:* , we need a new namespace for the V2 api. Since LBaaS is going
be  a seperate entity in the near future, we need to do the same thing in heat
for the LBaaS V2.

Proposed change
===============

We need to add the following LBaaS V2 heat resources.
1. LoadBalancer.
2. Listener.
3. Pool.
4. PoolMember.
5. HealthMonitor.

Specification.
--------------

1. LoadBalancer
---------------

LBaaS V2 LoadBalancer, which creates a LoadBalancer along with the VIP.

Namespace:
OS::LBaaS::LoadBalancer

Required Properties:
--------------------

vip_subnet:
  Subnet ID or name of the LoadBalancer’s VIP.
  String Value.
  Value must be of type neutron.subnet.

Optional Properties:
--------------------

name:
  Name of the LoadBalancer.
  String Value.
  Update allowed.

description:
  Description of the LoadBalancer.
  String Value.
  Update allowed.

provider:
  Provider of the LoadBalancer.
  String Value.

vip_address:
  IP address of the LoadBalancer.
  String Value.
  Value must be of type ip_addr.

admin_state_up:
  Administrative state of the LoadBalancer.
  String Value.
  Update allowed.

Attributes:
-----------

admin_state_up:
  Administrative state of the LoadBalancer.
provider:
  Provide of the LoadBalancer.
vip_address:
  VIP address of the LoadBalancer.
vip_subnet_id:
  VIP’s subnet id of the LoadBalancer.
listeners:
  List of listeners associated with the LoadBalancer.

2. Listener
-----------

LBaaS V2 Listener, which creates a Listener associated with the LoadBalancer
for a particular port and protocol.

Namespace:
OS::LBaaS:: Listener

Required Properties:
--------------------

protocol_port:
  Port of the Listener.
  Integer Value.
  Must be in the range of 0 to 65535

protocol:
  Protocol of the Listener.
  String Value.
  Allowed Values - TCP, HTTP, HTTPS, TERMINATED_HTTPS

loadbalancer:
  ID or name of the LoadBalancer to which Listener is associated with.
  String Value.
  Must be of type lbaas.loadbalancer.

Optional Properties:
--------------------

name:
  Name of the Listener.
  String Value.
  Update allowed.

description:
  Description of the Listener.
  String Value.
  Update allowed.

admin_state_up:
  Administrative state of the Listener.
  String Value.
  Update allowed.

default_tls_container_ref:
  Default TLS container reference to retrieve TLS information.
  Is mandatory if protocol is TERMINATED_HTTPS
  String Value.
  Update allowed.

sni_container_refs:
  List of TLS container references for SNI.
  List Value.
  Update allowed.

connection_limit:
  Max number of connections a listner can take.
  Intefer Value.
  Update allowed.
  Default value is -1.

Attributes:
-----------

protocol_port:
  Protocol port of the Listener.
protocol:
  Protocol of of the Listener.
loadbalancers:
  List of loadBalancers associated with the Listener.
admin_state_up:
  Administrative state of the Listener.
default_tls_container_ref:
  Default TLS container reference to retrieve TLS information.
sni_container_refs:
  List of TLS container references for SNI.

3. Pool
-------

LBaaS V2 Pool, which creates a Pool associated with the Listener.

Namespace:
OS::LBaaS::Pool

Required Properties:
--------------------

lb_algorithm:
  Load balancing algorithm to be used.
  String Value.
  Allowed Values - ROUND_ROBIN, LEAST_CONNECTIONS, SOURCE_IP
  Update allowed.

listener:
  ID or name of the listener to be associated with the Pool.
  String Value.
  Must be of type lbaas.listener.

protocol:
  Protocol of the Pool.
  String Value.
  Allowed Values - TCP, HTTP, HTTPS

Optional Properties:
--------------------

name:
  Name of the Pool.
  String Value.
  Update allowed.

admin_state_up:
  Administrative state of the Pool.
  String Value.
  Update allowed.

description:
  Description of the Pool.
  String Value.
  Update allowed.

session_persistence:
  Session persistence details of the Pool.
  String Value.
  Update allowed.

  Map properties:

    cookie_name:
      Name of the cookie.
      String Value.
      Required if the type is APP_COOKIE.

    type:
      Type of the session persistence.
      String Value.
      Allowed Values -  SOURCE_IP, HTTP_COOKIE, APP_COOKIE

Attributes:
-----------

admin_state_up:
  Administrative state of the Pool.
lb_algorithm:
  Load balancing algorithms of the LoadBalancer.
listeners:
  List of listener ID associated with the pool.
protocol:
  Protocol of the pool.

4. PoolMember
-------------

Backend servers to be added to the Load balancing pool.

Namespace:
OS::LBaaS::PoolMember

Required Properties:
--------------------

pool:
  ID or name of the pool that this member belongs to.
  String Value.
  Update allowed.
  Must be of type lbaas.pool.

address:
  IP address of the pool member in the pool.
  String Value.
  Value must be of type ip_addr.

protocol_port:
  Port on which the pool member listens for requests or connections.
  Integer Value.
  Must be in the range of 0 to 65535

subnet:
  Subnet ID or name for the member.
  String Value.
  Must be of type neutron.subnet

Optional Properties:
--------------------

weight:
  Weight of member in the pool.
  Integer Value.
  Must be in the range of 0 to 256.
  Update allowed.

admin_state_up:
  Administrative state of the PoolMember.
  String Value.
  Update allowed.

Attributes:
-----------

admin_state_up:
  Administrative state of the PoolMember.
weight:
  Weight of member in the pool.
address:
  IP address of the pool member in the pool.
pool_id:
  ID of the pool that this member belongs to.
protocol_port:
  Port on which the pool member listens for requests or connections.
subnet_id:
  Subnet ID for the member.

5. HealthMonitor
----------------

LBaaS V2 HealthMonitor, creates a health monitor for the Pool.

Namespace:
OS::LBaaS::HealthMonitor

Required Properties:
--------------------

delay:
  The minimum time in seconds between regular connections of member.
  Integer Value.
  Update allowed.

type:
  One of predefined health monitor types..
  String Value.
  Allowed values - PING, TCP, HTTP, HTTPS

max_retries:
  Number of permissible connection failures before changing the member status
to INACTIVE.
  Integer Value.
  Update allowed.
  Must be in the range of 1 to 10.

timeout:
  Maximum number of seconds for a monitor to wait for a connection to be
established before it times out.
  Integer Value.
  Update allowed.

pool:
  ID or name of the pool tobe monitored.
  String Value.
  Update allowed.
  Must be of type lbaas.pool.

Optional Properties:
--------------------

admin_state_up:
  The administrative state of the health monitor.
  String Value.
  Update allowed.

http_method:
  The HTTP method used for requests by the monitor of type HTTP.
  String Value.
  Update allowed.

expected_codes:
  The list of HTTP status codes expected in response from the member to
declare it healthy.
  String Value.
  Update allowed.

url_path:
  The HTTP path used in the HTTP request used by the monitor to test a member
health.
  String Value.
  Update allowed.

Attributes:
-----------

admin_state_up:
  The administrative state of this health monitor.
delay:
  The minimum time in seconds between regular connections of the member.
expected_codes:
  The list of HTTP status codes expected in response from the member to
  declare it healthy
http_method:
  The HTTP method used for requests by the monitor of type HTTP.
max_retries:
  Number of permissible connection failures before changing the member
  status to to INACTIVE.
timeout:
  Maximum number of seconds for a monitor to wait for a connection to be
  established before it times out.
type:
  One of predefined health monitor types.
url_path:
  The HTTP path used in the HTTP request used by the monitor.

References
----------

https://github.com/openstack/neutron-lbaas
https://github.com/openstack/heat
http://docs.openstack.org/developer/heat/template_guide/openstack.html
http://developer.openstack.org/api-ref-networking-v2-ext.html#lbaas-v2.0

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <bkalebe>

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

Add new namespace for the following resources.
OS::LBaaS::LoadBalancer
OS::LBaaS::Listener
OS::LBaaS::Pool
OS::LBaaS::PoolMember
OS::LBaaS::HealthMonitor

Dependencies
============

None
