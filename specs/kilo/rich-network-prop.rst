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
 For help with syntax, see http://sphinx-doc.org/rest.html To test out your
 formatting, see http://www.tele3.cz/jbar/rest/rest.html

======================================
OS::Nova::Server rich network property
======================================

https://blueprints.launchpad.net/heat/+spec/rich-network-prop

Allowing port and floating IP association properties to be specified within a
OS::Nova::Server works around issues with nova port management, provides
users with a simpler way of implementing a common pattern, and allows more
templates to be neutron/nova-networking agnostic.

Problem description
===================

There are a number of issues with OS::Neutron::Port which are currently
difficult to work around, including:

1. On server delete Nova deletes all ports, even those which were created
   before the nova boot (https://bugs.launchpad.net/nova/+bug/1158684).
   This causes issues on a stack-update since the port underlying a given
   port resource may no longer exist once the server has been replaced.

2. A port's relationship with a server is exclusive, however a stack-update
   which replaces a server will have the old and new servers attempting to
   attach to the same port resource

3. Two ports with the same fixed IP address cannot exist on the same network,
   so a stack-update which results in a port being replaced will fail
   unless the fixed IP address is changed too.

4. OS::Neutron::Port has a top-level ``network`` property but the ``subnet``
   is inside the ``fixed_ips`` property. If a network has multiple subnets
   and the port resource does not specify which subnet then neutron assigns
   the port to a non-deterministic subnet.

5. Users can avoid the above problems if they don't define an OS::Neutron::Port
   resource, but they must if they want to define a neutron floating IP
   association. Server+port+floating-ip is such a common pattern that users
   would benefit from being able to define all this in the server resource.

6. Likewise any template which associates servers with floating IPs will only
   work on either a neutron or nova-networking OpenStack.

Proposed change
===============

OS::Nova::Server has a networks property which allows a list of maps, where
the map key is one of ``fixed_ip``, ``network``, ``port`` or ``uuid`` which
map directly to nova boot nic options.

The proposed change is that new keys will be added to this map to support
fully describing ports within the ``networks`` items. The server resource
will take responsibility for creating and managing the port rather than
allowing nova to create the port implicitly.

* ``network`` *existing key* Name or UUID of network to create the nic on.
  Applies to neutron and nova-network.

* ``fixed_ip`` *existing key* Optional fixed IP address to assign to the
  nic. Applies to neutron and nova-network.

* ``subnet`` *new key* Name or UUID of neutron subnet to create the nic on.
  If specified then ``network`` is optional. If ``network`` is also specified
  then validation will confirm whether the subnet belongs to the network.
  Applies to neutron only.

* ``floating_ip`` *new key* ID of the floating IP to assign to this networks
  entry. The value can be a ref from a ``OS::Neutron::FloatingIP`` or
  ``OS::Nova::FloatingIP``. Or it can be provided a string from a parameter
  from an already existing floating IP. This property replaces
  OS::Neutron::FloatingIPAssociation and OS::Nova::FloatingIPAssociation so
  these resources which don't represent *real* resources can be deprecated.
  Applies to neutron and nova-network.

* ``port_extra_properties`` Map containing extra values to the neutron port
  creation which are not covered by the above or the derived properties.
  Applies to neutron only.

The implementation will be in the Server resource and will have different
paths based on ``self.is_using_neutron``.

Validation will be performed so that an error is raised if a value is set
that is not supported by nova-networking.

Server create in the neutron path will do the following:

* Limit the port to have at most one fixed_ip (neutron ports allow multiple
  fixed_ips). Users who require multiple fixed IPs can still create a full
  port resource.

* Derive the security groups from the Server property security_groups. This
  means that all created ports will be assigned to the same list of security
  groups.

* Derive the port name from the server name and the networks list position

* Create a port based on the passed and derived properties, and add that
  ``port-id`` to the nova ``nics`` list.

* Store the port-id for each created port in the resource data

Resource update in the neutron path will do the following:

* Calculate which ports to update, which to create and which to delete

Resource delete in the neutron path will delete any ports stored in the
resource data.

Special handling will be required for the following case:

* A stack update results in server replacement, and

* One of the ``networks`` items has specified a fixed_ip which doesn't change

In this case the handle_delete of the old server and the handle_create of the
new server will need to interact to allow the new port to be assigned the
fixed_ip which is assigned to the old port. Assigning back to the old port
may be required on rollback too.

Alternatives
------------

An alternative is to wait for bug #1158684 to be fixed in Nova, and make any
other necessary changes to OS::Neutron::Port and OS::Nova::Server to mitigate
the items listed in the `Problem description`_. (Items 4., 5. and 6. likely
wouldn't be addressed.

Implementation
==============

Assignee(s)
-----------

This blueprint needs a primary author to adopt it. Steve Baker will provide
implementation and review assistance if required.

Primary assignee:
  <skraynev>

Assisted by:
  <steve-stevebaker>

Milestones
----------

Target Milestone for completion:
  Kilo-2

Dependencies
============

There are no blueprint or library dependencies for this blueprint.
