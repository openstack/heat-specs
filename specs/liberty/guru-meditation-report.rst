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

===================================
 Adopt Oslo Guru Meditation Reports
===================================

https://blueprints.launchpad.net/heat/+spec/guru-meditation-report

This spec adopts Oslo Guru Meditation Reports in Heat. The feature will
enhance debugging capabilities of all Heat services, by providing
an easy and convenient way to collect debug data about current threads
and configuration, among other things, to developers, operators,
and tech support in production deployments.

Problem description
===================

Currently,Heat doesn't provide a way to collect state data from active service
processes. The only information that is available to deployers, developers,
and tech support is what was actually logged by the service. Additional data
could be usefully used to debug and solve problems that occur during Heat
operation. We could be interested in stack traces of green and real threads,
pid/ppid info, package version, configuration as seen by the service, etc.

Oslo Guru Meditation Reports provide an easy way to add support for collecting
the live state info from any service. Report generation is triggered by sending
a special(USR1) signal to a service. Reports are generated on stderr, and can
be piped into system log based on need.

Nova has supported Oslo Guru Meditation Reports.

Proposed change
===============

First, the oslo-incubator module (reports.*) should be synchronized into
heat tree. Then, each service process needs to initialize the error report
system prior to the service start().

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  zhangtralon

Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

* sync reports.* module from oslo-incubator
* adopt it in all heat services under heat/bin/
* add some developer docs on how to use this feature

Dependencies
============

[1] oslo-incubator module: http://git.openstack.org/cgit/openstack/oslo-incubator/tree/openstack/common/report
[2] nova guru meditation reports: https://blueprints.launchpad.net/nova/+spec/guru-meditation-report
[3] blog about nova guru reports: https://www.berrange.com/posts/2015/02/19/nova-and-its-use-of-olso-incubator-guru-meditation-reports/
[4] oslo.reports repo: https://github.com/directxman12/oslo.reports
