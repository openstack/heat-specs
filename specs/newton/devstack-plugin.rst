..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================
Devstack plugin support
=======================

https://blueprints.launchpad.net/heat/+spec/heat-support-devstack-plugin

DevStack supports a standard mechanism for including plugins from external
repositories. So add devstack plugin for heat.

Problem description
===================

Devstack support external plugins as documented here:
http://docs.openstack.org/developer/devstack/plugins.html
By enabling this plugin, we just need to properly set up devstack
local[rc] file to be able to setup heat.
A good example is ironic one:
https://review.openstack.org/#/q/topic:ironic-devstack-plugin

Proposed change
===============

1. Introduce devstack plugin.

   An external git repository that includes a devstack/ top level directory.
   Inside this directory there can be the following files::

        devstack/
            override-defaults
            settings
            plugin.sh
            lib/

    plugin.sh is the actual plugin. It is executed by devstack at well defined
    points during a stack.sh run.

    Plugins are registered by adding the following to the localrc section of
    local.conf. They are added in the following format::

        [[local|localrc]]
        enable_plugin heat https://git.openstack.org/openstack/heat

   The detailed introduction is here:
   http://docs.openstack.org/developer/devstack/plugins.html

2. Steps to support devstack plugin in heat.

step1: Copy devstack code to heat tree.

step2: Add devstack plugin
This adds the actual devstack plugin, devstack should not run the heat code
in the devstack tree.

step3: Add a heat job to use devstack plugin.
After heat has a devstack plugin in tree. Make a job to be able to test that
it works, non-voting, before we actually switch everything over and drop the
devstack code.

step4. Switch all heat jobs to use devstack plugin

step5. Remove heat code from project openstack-dev/devstack


Alternatives
------------

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  dixiaoli <dixiaobj@cn.ibm.com>

Milestones
----------

Target Milestone for completion:
  newton-1

Work Items
----------

- Copy devstack code to heat tree.
- Add devstack plugin
- Switch all heat jobs to use devstack plugin
- Remove heat code from project openstack-dev/devstack

Dependencies
============
