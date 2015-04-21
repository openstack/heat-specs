..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


=============================
 Attribute Type in schema
=============================

https://blueprints.launchpad.net/heat/+spec/add-type-in-attributes-schema

This Blueprint proposes to add type field to attribute schema.

Problem description
===================

Currently there is no way to find out what is the type of attribute returned
by the get_attr function. This makes it difficult for the template authors to
figure out what type of value will be returned. Indexing and Mapping on the
attributes also becomes a issue without the knowledge of the attribute type.

Proposed change
===============

The changes will be made in each resource plugin to add type field in the
attribute schema. Type can be a String, Map or List. This will also generate
the docs telling the users what type of value to expect from get_attr.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ishant-tyagi
  rakesh_hs

Milestones
----------

Target Milestone for completion:
  Liberty-1

Work Items
----------

* Add type field in schema of each resource plugin.

Dependencies
============

None
