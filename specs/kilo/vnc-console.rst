..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

===================================
 Nova Server VNC Console Attribute
===================================

Launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/vnc-console-attr


Problem description
===================

As an end user, if I want to retrieve the vnc console url of a server
resource in heat stack, I need to combine `heat resource-list` and
`nova get-vnc-console` to get the result. For example::

  heat resource-list <stack_name> # get physical_resource_id
  nova get-vnc-console <physical_resource_id> <vnc_console_type>

We should provide a way for template developers to show console
url(for example, vnc, rdp and spice) in stack outputs.

Usage Scenario
==============

Get novnc console url::

   heat_template_version: 2013-05-23
   resources:
     server:
       type: "OS::Nova::Server"
       properties:
         image: fedora
         key_name: heat_key
         flavor: m1.small
   outputs:
     vnc_console_url:
       value:
         get_attr: [server, console_urls, novnc]

So the novnc console url can be retrieved via `heat output-show
<stack> vnc_console_url`.

Get xvpvnc console url::

   heat_template_version: 2013-05-23
   resources:
     server:
       type: "OS::Nova::Server"
       properties:
         image: fedora
         key_name: heat_key
         flavor: m1.small
   outputs:
     vnc_console_url:
       value:
         get_attr: [server, console_urls, xvpvnc]

So the xvpvnc console url can be retrieved via `heat output-show
<stack> vnc_console_url`.

Get spice console url::

   heat_template_version: 2013-05-23
   resources:
     server:
       type: "OS::Nova::Server"
       properties:
         image: fedora
         key_name: heat_key
         flavor: m1.small
   outputs:
     spice_console_url:
       value:
         get_attr: [server, console_urls, spice-html5]


Proposed change
===============

Add composite attribute `console_urls` to `OS::Nova::Server` resource.
When `get_attr` is invoked, return the console URL according the key supplied
to this attribute, or URLs for all supported types when no key is provided.
Gracefully deal with the case when the type of the console being asked for
is not available in current deployment.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  pshchelo


Milestones
----------

Target Milestone for completion:
  Kilo-1

Work Items
----------

- implement `get_console_urls` method in Nova client plugin;
- add `console_urls` attribute to OS::Nova::Server resource.


Dependencies
============

No dependency on other spec or additional library.
