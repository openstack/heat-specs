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

=====================
StackDefinition class
=====================

https://blueprints.launchpad.net/heat/+spec/stack-definition

Encapsulate all data about the definition of the stack - including the
template, parameter values, resource attributes & reference IDs - in a class
and use that in intrinsic functions instead of the Stack object itself.

Problem description
===================

A number of problems arise from the fact the we pass the
heat.engine.stack.Stack object representing the stack to Template.parse() (and
thence to the Function objects) in order to provide access to data needed to
define the stack.

The main issue is that the so-called 'lightweight stack', used in convergence
when performing a check on a single resource, is not particularly lightweight.
In particular, in order for the resource being checked to use an attribute or
resource ID from another resource we create a heat.engine.resource.Resource
object for every resource in the stack. This occurs even though the actual
values we need are passed in over RPC and none of the Resource object's data is
actually loaded from the database, nor any of its code used. Eliminating
loading the data from the database reduced memory use by 10%, and further
savings are likely from not creating O(n^2) Resource objects in the course of a
graph traversal.

In addition, using the Stack object in this way makes it extremely unclear what
part of the interface is stable for the purposes of third-party Template
plugins and their associated Functions. Developers don't know which aspects of
the Stack interface they need to preserve across versions, and plugin
developers don't know what they can rely on. Many of the potential operations
that the Stack class makes possible may, in fact, be horrifically inefficient
in the convergence architecture, or may become so in future.

Proposed change
===============

Create a new StackDefinition class that encapsulates the data needed to define
the stack. Pass this object to Template.parse() in place of the Stack object.

When a resource is accessed via the StackDefinition, return a ResourceProxy
object that contains the pertinent data only.

For all intents and purposes, the initial API will comprise whatever parts of
the Stack and Resource classes that are currently used by intrinsic functions
in the HOT or Cfn Template plugins. Existing interfaces will be maintained, so
that no code changes are required for any plugins using this subset of the
functionality. This includes:

* Template

  * Environment

    * Parameter values

* Resources

  * Name
  * Status
  * Action
  * Attributes
  * Reference ID
  * DB ID
  * UUID

* Parent (facade) resource

  * Metadata
  * Template

In convergence when checking a resource, only those other resources on which
there is a direct dependency will have a proxy available, and only attributes
required by the current resource (as returned by the function.dep_attrs()
function) will have values available.

Unless mentioned specifically above, no other data will be available from the
StackDefinition. This will potentially break third-party Template plugins, but
it is impossible to know to what extent this is a problem due to the undefined
surface area of the current stable API. However, anything relying on behaviour
outside of the proposed API is quite possibly highly inefficient, and
completely untested in upstream Heat. On balance, it's worth tolerating this
breakage, early in a development cycle, in order to move to a guaranteed stable
API. Third-party Template plugin developers have the opportunity to weigh in on
this spec with requests.

Future changes to the API (beyond Pike) will require a deprecation period.

Alternatives
------------

Just put up with it the way it is?

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  zaneb

Milestones
----------

Target Milestone for completion:
  pike-1

Work Items
----------

- Encapsulate in a NodeData class the data that convergence records about a
  node in the graph after traversing it.
- Teach Resource to generate its own NodeData.
- Create a ParentResourceProxy to encapsulate data about the facade resource
  and potentially load it independently of the parent stack.
- Move the Stack's template and other data into a StackDefinition class and
  proxy any requests for that data to it.
- Update the NodeData after processing each Resource in the legacy path.
- Pass the StackDefinition in place of the Stack to Template.parse().

Dependencies
============

None
