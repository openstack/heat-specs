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

==============================
 Multiple Environment Support
==============================

https://blueprints.launchpad.net/heat/+spec/multi-environments

We allow the user to specify multiple environment files in the client, but
these get combined in the client so any redundant information, precendence, &c.
is no longer available to heat-engine. This causes problems with PATCH updates
of the environment, particularly with TripleO.

Problem description
===================

On a PATCH update for a stack whose environment is a composite from multiple
files, a user cannot (in the general case) safely update any of the environment
files without explicitly passing all of the files previously included to the
client again (since order matters, and since the engine has no knowledge of any
given file's position in the hierarchy. This leaves them in a similar position
to where they would be without PATCH updates to the environment: having to
remember all of the constituent parts of the stack's environment.

This is a particular problem for TripleO, which may use many environment files
even in a fairly typical deployment. If the user customises one of the default
environment files, the change is not picked up because the TripleO client does
not send environment files with its PATCH updates unless they are explicitly
specified; conversely sending the default environment file(s) again risks
overwriting user-specified environment (such as the one for network isolation)
unless the user is required to always pass all of the environment files again.

Proposed change
===============

Add an optional "environment_files" key to the body of a stack create or update
request. Valid content for this key is a list of filenames. The filenames
themselves may be arbitrary. The file content must be included in the "files"
section of the request, keyed by the filename, in the same way as other extra
files (scripts, nested templates) are.

The "environment_files" key is outside the existing environment section to
ensure that it is only inserted by the client; this change does not modify the
environment file format itself. This prevents any issues with circular
inclusions and the like.

Multiple files will be combined by the engine in the same manner as they
currently are by the client. Where environment files contain conflicting
information, the last one specified wins.

Parameter values that are specified explicitly (i.e. outside the environment)
will be applied *after* all environment files are merged, to maintain
consistency with the current approach (where the file combination is done in
the client and the parameters merged in heat-api). This means that the code to
do this must be moved from heat-api to heat-engine.

On a PATCH update, any additional_environment files specified are appended to
the list. Heat will recalculate the combined environment on each stack update,
so that any changes to the "files" part of the environment are picked up.

Alternatives
------------

We could allow includes in the environment file format itself. However, this
would require us to deal with problems like circular includes, or to have a
different format for the included environment files vs. the 'main' environment.
While it would be nice to be able to record all of the environments for a given
stack in a single place that can be stored e.g. in Git, it's probably better to
implement this purely on the client side as a CLI option to read the list of
environments from a file instead of/as well as from multiple --environment
options.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  jdob

Milestones
----------

Target Milestone for completion:
  Mitaka-1

Work Items
----------

* Add support for combining environments + parameters in heat-engine
* Add support for passing the environment_files list + params over the RPC API
* Add support for environment_files in heat-api
* Modify the client to pass environments as a list
* Add a CLI option to read the environments list from a file

Dependencies
============

None.
