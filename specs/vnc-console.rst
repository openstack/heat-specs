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

We should provide a way for template developers to show vnc console
url in stack outputs.

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
         get_attr: [server, vnc_console_url]

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
         vnc_console_type: xvpvnc
   outputs:
     vnc_console_url:
       value:
         get_attr: [server, vnc_console_url]

So the xvpvnc console url can be retrieved via `heat output-show
<stack> vnc_console_url`.


Proposed change
===============

Add property `vnc_console_type` and attribute `vnc_console_url` in
`OS::Nova::Server` resource. When `get_attr` is invoked, return the
vnc console url according `vnc_console_type`.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  nanjj



Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------

small enough change.


Dependencies
============

No dependency on other spec or additional library.
