from setuptools import setup, find_packages

from ckanext.dgutheme import __version__

setup(
    name='ckanext-dgutheme',
    version=__version__,
    long_description="""\
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    namespace_packages=['ckanext', 'ckanext.dgutheme'],
    zip_safe=False,
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    license='Presentation: GPLv2; Python: AGPL',
    url='http://ckan.org/',
    description='CKAN DGU theme extension',
    keywords='data packaging component tool server',
    install_requires=[
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={'ckan': ['i18n/*/LC_MESSAGES/*.mo']},
    entry_points="""
        [ckan.plugins]
        dgu_theme_embedded = ckanext.dgutheme.plugin:EmbeddedThemePlugin
        dgu_theme_independent = ckanext.dgutheme.plugin:IndependentThemePlugin
    """,
    test_suite = 'nose.collector',
)
