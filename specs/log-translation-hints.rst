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

==================================
Add log translation hints for Heat
==================================

https://blueprints.launchpad.net/Heat/+spec/log-translation-hints

To update Heat log messages to take advantage of oslo's new feature of
supporting translating log messages using different translation domains.

Problem description
===================

Current oslo libraries support translating log messages using different
translation domains and oslo would like to see hints in all of our code
by the end of juno. So Heat should handle the changes out over the release.

Proposed change
===============

Since there are too many files need to change, so divide this bp into dozens of
patches according to Heat directories(which need applying this change).

For each directory's files, we change all the log messages as follows.

1. Change "LOG.error(_(" to "LOG.error(_LE".

2. Change "LOG.warn(_(" to "LOG.warn(_LW(".

3. Change "LOG.info(_(" to "LOG.info(_LI(".

4. Change "LOG.critical(_(" to "LOG.critical(_LC(".

Note that this spec and associated blueprint are not to address the problem of
removing translation of debug messages.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  liusheng<liusheng@huawei.com>

Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------

For each directory's files, we change all the log messages as follows.

1. Change "LOG.error(_(" to "LOG.error(_LE".

2. Change "LOG.warn(_(" to "LOG.warn(_LW(".

3. Change "LOG.info(_(" to "LOG.info(_LI(".

4. Change "LOG.critical(_(" to "LOG.critical(_LC(".

We handle these changes in the following order::

    ├── contrib           #TODO1
    ├── heat
    │   ├── api        #TODO2
    │   ├── cloudinit  #TODO3
    │   ├── cmd
    │   ├── common     #TODO4
    │   ├── db         #TODO5
    │   ├── doc
    │   ├── engine     #TODO6
    │   ├── locale
    │   ├── openstack  #TODO7
    │   ├── rpc        #TODO8
    │   ├── scaling    #TODO9
    │   ├── tests      #TODO10

Add a HACKING check rule to ensure that log messages to relative domain.
Using regular expression to check whether log messages with relative _L*
function.

::

    log_translation_domain_info =re.compile(
        r"(.)*LOG\.info\(\s*_LI\(('|\")")
    log_translation_domain_warning = re.compile(
        r"(.)*LOG\.(warn|warning)\(\s*_LW\(('|\")")
    log_translation_domain_error = re.compile(
        r"(.)*LOG\.error\(\s*_LE\(('|\")")
    log_translation_domain_critical = re.compile(
        r"(.)*LOG\.critical\(\s*_LC\(('|\")")

Dependencies
============

[1]https://blueprints.launchpad.net/oslo/+spec/log-messages-translation-domain-rollout

[2]https://wiki.openstack.org/wiki/LoggingStandards
