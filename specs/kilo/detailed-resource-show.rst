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

======================
Detailed Resource Show
======================

https://blueprints.launchpad.net/heat/+spec/detailed-resource-show

After creating a stack, there is currently no way to retrieve a resource's
attributes other than outside of heat (e.g. a user can get the ID of a nova
server and call nova directly to get such attributes).

Problem description
===================

Currently a template author needs to explicitly define in the outputs section
which attributes they'll need access to after a stack is created. Without doing
so, the attributes cannot be retrieved anymore unless the user updates the
template to add such attributes to the outputs section and update the stack
afterwards.

Proposed change
===============

Since the attributes of a resource are really being retrieved by heat using the
resource client, that means the user can get the resource ID from heat and
interact directly with the client (e.g. get the ID of a nova server and talk
directly to nova) to retrieve its attributes.

We propose returning all resource attributes when displaying data for a
specific resource.  This way, a user will be able to issue a resource-show call
and be able to look up attributes after creating their stacks even if the
template author didn't think about them beforehand.

Because these attributes can be retrieved either by the resource's client or by
changing the template and adding them to the outputs section, this should not pose
any more risk of revealing sensitive data than what is already possible.

This can be achieved by changing the API response to also include attributes
that can be automatically discovered (i.e. resources that have an attributes
schema).

  # API
  # the call below would also return all attributes in the resource schema
  /<tenant_id>/stacks/<stack_name>/<stack_id>/resources/<resource_name>

However, some resources have dynamic attributes that cannot be discovered using
their attributes schema, so this approach won't work for those resources.  For
instance, ``OS::Heat::ResourceGroup`` has dynamic attributes based on what
outputs/attributes the group type exposes and ``OS::Heat::SoftwareDeployments``
has an attribute for each output defined in the config resource outputs
property.

For such resources, the API can be extended to accept a query param that will
hold the names of the attributes to be retrived.  Something like:

  # API
  /<tenant_id>/stacks/<stack_name>/<stack_id>/resources/<resource_name>?with_attr=foo&with_attr=bar

  # heatclient
  resource-show <stack_name> <resource_name> --with-attr foo --with-attr bar

However, certain clients or scripts may want to consume a given attribute
directly.  For these cases, we could also add two new endpoints: one to keep
things RESTful and return only the discoverable attributes of a resource; and
another one that would only return the value of the requested attribute.

  # API
  /<tenant_id>/stacks/<stack_name>/<stack_id>/resources/<resource_name>/attributes
  /<tenant_id>/stacks/<stack_name>/<stack_id>/resources/<resource_name>/attributes/<attribute_name>

  # heatclient
  heat resource-attributes <stack-id> <resource-name>
  heat resource-attributes <stack-id> <resource-name> <attribute-name>

Alternatives
------------

Alternatively, we can keep the current resource-show behavior the same and only
add the two new endpoints to return the attribute information.  This has the
benefit of being simpler to implement, as only changes to add the new endpoint
would be needed.  However, the drawback is that one would have to make two
separate calls to get all the available information on a given resource: one to
resource-show and another one to resource-attributes.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  andersonvom
  asifrc

Milestones
----------

Target Milestone for completion:
  Kilo

Work Items
----------

* Add resource attributes to the engine API at format time.


Dependencies
============

None
