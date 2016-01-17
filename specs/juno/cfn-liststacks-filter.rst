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

==============================================
Add filter support to stack query for cfn API
==============================================

https://blueprints.launchpad.net/heat/+spec/cfn-liststacks-filter

Currently filtering stacks by status is supported in openstack API, for
the compatibility with Cloudformation API, it also should be supported
in cfn API.

Problem description
===================

User want to query the stack list and filter them by status, which is already
implemented in openstack API, we also need to implement it in cfn API.

Proposed change
===============

Add parameter "StackStatusFilter" for list-stacks of cfn API, and pass
the fiter parameters to the backend, then return the stacks filtered by status.
The url should be like this::

    https://example.com:8000/v1/
         ?Action=ListStacks
         &StackStatusFilter.member.1=CREATE_IN_PROGRESS
         &StackStatusFilter.member.2=DELETE_COMPLETE
         &Version=2010-05-15
         &SignatureVersion=2
         &SignatureMethod=HmacSHA256
         &Timestamp=2010-07-27T22%3A26%3A28.000Z
         &AWSAccessKeyId=[AWS Access KeyID]
         &Signature=[Signature]

Alternatives
------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  neil-zhangyang

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

* update api of liststacks in cfn API, allow user filter stacks by status
* update cfn API document
* add a functional test in tempest/thirdparty/boto

Dependencies
============

- https://launchpad.net/heat/+spec/filter-stacks

