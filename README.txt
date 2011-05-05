=====================-----==============
ckanext-dgutheme - data.gov.uk extension
========================================


Dependencies
============


Setup
=====

You need ckan installed in the same virtual environment::

    virtualenv pyenv
    pip -E pyenv install -e .
    pip -E pyenv install -e hg+http://bitbucket.org/okfn/ckan#egg=ckan



Configuration
=============

Each theme is activated by naming the plugin in the
CKAN configuration file (.ini) in the [app:main] section

e.g.
    ckan.plugins = dgu_theme_embedded


Documentation
=============

DGU is an extension for CKAN: http://ckan.org
