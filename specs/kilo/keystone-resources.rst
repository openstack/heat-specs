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

=========================
Native Keystone Resources
=========================

https://blueprints.launchpad.net/heat/+spec/keystone-resources

Problem description
===================

Some cloud operators would like to be able to use Heat templates to manage
users, projects and roles in Keystone. Currently we can only create users, and
only through an AWS IAM resource type.

This was discussed on the mailing list in the thread beginning here:

http://lists.openstack.org/pipermail/openstack-dev/2015-January/055554.html

Proposed change
===============

Implement the following native resource types:

* OS::Keystone::User

  * name (optional - defaults to self.physical_resource_name())
  * default_project_id (optional)
  * email (optional)
  * domain (optional)
  * password (optional)
  * enabled (default True)
  * groups (list)
  * roles (list)

    * domain (optional - domain or project or both must be specified)
    * project (optional - domain or project or both must be specified)
    * role

* OS::Keystone::Group

  * name (optional - defaults to self.physical_resource_name())
  * domain (optional)
  * description (optional)
  * roles (list)

    * domain (optional - domain or project or both must be specified)
    * project (optional - domain or project or both must be specified)
    * role

* OS::Keystone::Role

  * name (optional - defaults to self.physical_resource_name())

* OS::Keystone::Project

  * name (optional - defaults to self.physical_resource_name())
  * domain (optional)
  * description (optional)
  * enabled (default True)

Since in the default policy.json configuration these APIs are available only to
administrative users, the plugin would be in the /contrib tree and not
installed by default.

Alternatives
------------

Another possible data model would be to have a separate RoleAssignment resource
(or similar) to grant roles to users or groups, rather that having the roles
listed in the user or group resources. A similar thing could apply to the list
of users in a group, which could be implemented instead as a GroupMembership
resource.

However, there are a couple of problems with that data model. The first is that
adding a user to a group or granting a role to a user/group does not create a
physical resource with its own UUID. This makes it difficult for Heat to manage
the resources.

The second issue is that such an approach tends to create dependency problems
for users - for example in this model if another resource depends on a User,
then Heat may begin creating it before the User has been assigned a Role that
it may need to perform the operation. This is possibly less of an issue with
Keystone resources than it has proven with Neutron resources, but it is a known
anti-pattern in Heat data modelling.

A similar issue occurs with Users and Groups - an alternative implementation
would be for the Group definition to contain a list of Users rather than for
the User definition to contain a list of Groups. The advantage of that is that
it more closely follows how the API is implemented, but this way was chosen
because it is more likely to automatically generate correct dependencies:
anything that depends on a User will always wait for all groups to be assigned.
Both approaches are likely to make some (different) subset of use cases
awkward, but the only solution would be a separate GroupMembership resources
type and that would suffer from all of the problems with a RoleAssignment
discussed above.

Implementation
==============

Assignee(s)
-----------

Primary Assignee:
  kanagaraj-manickam

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- User plugin
- Project plugin
- Group plugin
- Role plugin
- Custom constraint for keystone.project
- Custom constraint for keystone.group
- Custom constraint for keystone.role
- Custom constraint for keystone.domain

Dependencies
============

None
