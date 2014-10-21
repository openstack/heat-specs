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

====================================================
 Reorganize the code structure of resources folder
====================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/reorganize-resources-code-structure

Reorganize the resources code structure to make it more clear.

Problem description
===================

The code structure of the resources folder is in some confusion.

Proposed change
===============

The new code structure will be::

    heat
    |----engine
    |----resources
         |----aws
              |----ec2
                   |----res1
                   |----res2
              |----autoscaling
                   |----res1
                   |----res2
         |----openstack
              |----nova
                   |----res1
                   |----res2
              |----neutron
                   |----res1
                   |----res2
              |----cinder
                   |----res1
                   |----res2


Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  huangtianhua <huangtianhua@huawei.com>

Milestones
----------

Target Milestone for completion:
  Kilo-2

Work Items
----------

* Put the AWS resources to folder resources/aws
* Put the OpenStack resources to folder resources/openstack

Dependencies
============

https://blueprints.launchpad.net/heat/+spec/decouple-aws-os-resources

