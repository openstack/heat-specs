=============================
OpenStack Heat Specifications
=============================

This git repository is used to hold approved design specifications for
additions to the heat project. Reviews of the specs are done in gerrit,
using a similar workflow to how we review and merge changes to the code
itself.

The layout of this repository is::

  specs/<release>/

Specifications are proposed for a given release by adding them to the
`specs/<release>` directory and posting it for review.  The implementation
status of a blueprint for a given release can be found by looking at the
blueprint in launchpad.  Not all approved blueprints will get fully
implemented.

You can find an example spec in `specs/template.rst`.

There is a sub-directory specs/<release>/backlog to store all specs
that had been approved but are not implemented in a specific release.

Movement of specs to the backlog would be done in a batch at the end of
a release cycle.

Prior to the Juno development cycle, this repository was not used for spec
reviews.  Reviews prior to Juno were completed entirely through Launchpad
blueprints::

  http://blueprints.launchpad.net/heat

Please note, Launchpad blueprints are still used for tracking the
current status of blueprints. For more information, see::

  https://wiki.openstack.org/wiki/Blueprints

For more information about working with gerrit, see::

  http://docs.openstack.org/infra/manual/developers.html#development-workflow

To validate that the specification is syntactically correct (i.e. get more
confidence in the Jenkins result), please execute the following command::

  $ tox

After running ``tox``, the documentation will be available for viewing in HTML
format in the ``doc/build/`` directory. Please do not checkin the generated
HTML files as a part of your commit.
