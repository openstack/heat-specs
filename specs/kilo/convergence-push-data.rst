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

=====================================================
Extract data from resources to push into dependencies
=====================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-push-data

Problem description
===================

We currently assume that every resource in a stack is loaded in memory
concurrently, and we query it directly to determine its attribute values. This
'pull' system is inefficient in the convergence architechture compared to a
'push' system, since we hope to typically have only one resource loaded in
memory at a time.

Proposed change
===============

Analyse the template to determine which attributes of a resource are needed
elsewhere. This is conceptually quite similar to the way we analyse the
template looking for dependencies, by recursively examining a snippet of
template and building up a list of dependent resources, except that instead of
only a list of resources we'll need to include the attribute names being
referenced. In this way the code will be able to work with arbitrary template
format plugins, although it will probably require a change to the Function
plugin API. Return the result as a mapping from resource names to a list of
referenced attribute names.

After a create or update event, we can use this list of attributes to query the
resource for all of the information that will be needed subsequently from it.

Alternatives
------------

Load a resource from the database whenever we need to retrieve one of its
attributes.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  skraynev

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Determine the list of attributes of a resource which are referenced in the
  template


Dependencies
============

None
