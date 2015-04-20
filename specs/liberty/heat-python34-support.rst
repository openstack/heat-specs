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

================
Python34 Support
================

https://blueprints.launchpad.net/heat/+spec/heat-python34-support

This spec aims to bring Python 3.4 support to Heat.

Problem description
===================

Heat isn't compatible with Python3.x. The blocker for Heat to migrate
was eventlet and now that eventlet fully supports python3, it is possible
for us to run Heat unit tests in a Python 3.4 environment. Once
all the dependencies of Heat are all functionally Python3 compatible, we
should be able to run integrationtests against Heat in a devstack environment.

Proposed change
===============

The first step towards Python 3.4 compatibility for Heat would be to
get the unit tests running successfully in a py34 environment. We need
to add a new py34 environment in tox for this and start testing individual
test files. To avoid regressing on old test files, we should add a separate
file which will consist of all the test files that have already been
verified in a Python3 environment.

All of these changes are not supposed to break existing unit tests nor
change the functionality in any way. The existing gate tests should take
care of this.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  sirushtim

Milestones
----------

Target Milestone for completion:
  liberty-1, could stretch to liberty-2 depending on how many
  incompatibilities exist while running tests.

Work Items
----------
- Use 2to6 partially to automatically fix some incompatibilities and satisfy
  flake8.
- Create a tox py34 env that will run off a meta-testfile which will consist
  of test file names that have already been verified to work with py34. This
  env will also use a different requirements file since there are two
  dependencies qpid-python and MySQL-python which aren't currently Python3
  compatible.
- Add a voting python34-partial gate job that will run the above env.
- Migrate all the unit tests to be compatible with Python 3.4 either one-by-one
  or migrate tests in alphabetical order, whichever is reasonably sized and
  easier to review. This also means we will fix the modules/files that each
  test case imports to test and make them python34 compatible.
  While migrating the tests, the strategy with mox is to use mox3 instead of
  converting them to mock as much as possible.
- Once migration is complete for all the tests, delete the meta-testfile and
  rename the gate job to gate-heat-python34.
- Remove dependencies on qpid-python and MySQL-python and merge
  requirements.txt for python-2.7 and python-3.4.
- Once dependencies of Heat are functionally Python 3.4 compatible, create a
  DevStack gate job which will run the Python 3.4 version of Heat.

Dependencies
============
Current dependencies of Heat that are/were not compatible with Python 3.4:

requirements.txt
- qpid-python: Used in install.sh. Can be removed.
- PasteDeploy: Needs to be functionally tested. The tests pass on Python 3.4
and the classifiers were just added.[1]
- oslo.messaging: Some of the drivers/executors don't work at the moment
but are being worked on by Victor Stinner.
- oslo.db: MySQL-python dialect isn't compatible with Python 3.4. There's a
Python 3.4 port for MySQL-python however.
- sqlalchemy-migrate: There's PY34 tests running for every patch of
sqlalchemy-migrate and the classifiers will be added for it.[2]

test-requirements.txt
- MySQL-python: ditto - oslo.db^. Can be removed.
- mox: needs to be replaced by mox3 until we move to mock completely.

[1] https://bitbucket.org/ianb/pastedeploy/commits/f30a7d518c6a79fcddfbe3f622337f81e41cb6a5
[2] https://review.openstack.org/#/c/174738/
