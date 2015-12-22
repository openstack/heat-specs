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

=================================================
 Usablity enhancements to the user's environment.
=================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/env-nested-usability

There a number of related enhancements that we can easily do in the
way the environment interacts with template resources, lets quickly
solve these for our users, to make heat more useable.
These issues have been raised here:
https://etherpad.openstack.org/p/heat-useablity-improvements


Problem description
===================

Here are some small problems that are related to the interaction of
the environment and template resources. They are grouped here to
reduce the red-tape.


No way to specify "global" parameters
-------------------------------------
When creating deep and/or complex compositions of multiple provider
templates, it becomes cubmersome if you end up passing a long list
of common parameters down through the "layers" via
properties/parameters.  If the environment had a "global_parameters"
section, you could specify those parameters which should be visible
to not only the top-level stack, but all child stacks too.


There is no way to transparently replace a resource with a provider resource.
-----------------------------------------------------------------------------
When, for example, you replace OS::Nova::Server with
OS::My::SpecialServer via a provider resource mapped in the
environment, you can't use the overloaded special server
transparently, because when you do get_resource: special_server, you
get a nested stack ID, not the nested server ID.


Required mirroring of resource attributes.
------------------------------------------
It is a pain to require the user to mirror a nested stack's resource
attributes in the outputs so they can be referenced outside of the
nested stack. We should generate these attributes dynamically.


Proposed change
===============

1. Add the concept of parameter_defaults to the environment.
   This will look like the following::

     parameter_defaults:
       flavor: m1.small
       region: far-away

   The behaviour of these parameters will be as follows:
   - if there is no parameter definition for it, it will be ignored.
   - these will be passed into all nested templates
   - they will only be used as a default so that they can be explicitly
   overridden in the "parameters" section.

2. Support a specially named output to Template resources that is used
   for references.

Modify the FnGetRefId of TemplateResource to look for an output called
"OS::stack_id", if this is provided then return this, else the current
value.


3. Add dynamic attributes to template resources.

A reminder of what the resource group does::

  {get_attr: [a_resource_group, resource.<res number>.attr_name]}

For template resources the following will be supported::

  {get_attr: [a_resource_templ, resource.<res name>.attr_name]}

To achieve this, _resolve_attribute() will be overridden to look for
"resource.<res name>" and then drill down to that resource's attribute.


Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  asalkeld


Milestones
----------

Target Milestone for completion:
  Kilo-2

Work Items
----------

Each item can be completed seperately.
Documentation for each feature needs to be added to the template guide.

Dependencies
============

None
