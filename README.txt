========================================
ckanext-dgutheme - data.gov.uk extension
========================================
Provides the theming of CKAN for the data.gov.uk extenstion, ckanext-dgu.  This
means providing the css stylesheets, and also modifications to the html
templates.

Dependencies
============
Although not a dependency, it probably makes sense to install the ckanext-dgu
extension:

	https://github.com/okfn/ckanext-dgu.git

Setup
=====
You need ckan installed in the same virtual environment::

    virtualenv pyenv
    pip -E pyenv install -e .
    pip -E pyenv install -e git+https://github.com/okfn/ckan.git#egg=ckan

Configuration
=============
The theme is activated by declaring it in the [app:main] section of the CKAN
config file: ::

	ckan.plugins = dgu_theme


Documentation
=============
DGU is an extension for CKAN: http://ckan.org
