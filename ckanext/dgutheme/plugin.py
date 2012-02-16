import re
import os

from logging import getLogger

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, IRoutes, IPackageController
import ckanext.dgutheme

log = getLogger(__name__)

def configure_template_directory(config, relative_path):
    configure_served_directory(config, relative_path, 'extra_template_paths')

def configure_public_directory(config, relative_path):
    configure_served_directory(config, relative_path, 'extra_public_paths')

def configure_served_directory(config, relative_path, config_var):
    'Configure serving of public/template directories.'
    assert config_var in ('extra_template_paths', 'extra_public_paths')
    this_dir = os.path.dirname(ckanext.dgutheme.__file__)
    absolute_path = os.path.join(this_dir, relative_path)
    if absolute_path not in config.get(config_var, ''):
        if config.get(config_var):
            config[config_var] = absolute_path + ',' + config[config_var]
        else:
            config[config_var] = absolute_path


class ThemePlugin(SingletonPlugin):
    '''
    DGU Visual Theme for a CKAN install embedded in dgu/Drupal.
    '''
    implements(IConfigurer)
    implements(IRoutes)

    def update_config(self, config):
        configure_template_directory(config, 'theme/templates')
        configure_public_directory(config, 'theme/public')

        config['package_form'] = 'package_gov3'

    def before_map(self, map):
        """
        Connect the homepage to "/data".

        This is just for demonstration.  In deployment, CKAN will be
        hosted at "/data".  Making this unecessary.
        """
        map.connect('/data', controller='home', action='index')
        # map.connect('/data', controller='ckanext.dgu.controllers.catalogue:CatalogueController', action='home')
        return map

    def after_map(self, map):
        return map

class SearchPlugin(SingletonPlugin):
    """
    DGU-specific searching.

    One thing DGU specific about the search is that DGU facets on
    whether a dataset's licenese_id is OGL (Open Government License) or not.
    Since this is calcuable from the license_id, but is not a facet over the
    whole set of possible license_id values (ie. 'ukcrown', 'other' etc. should
    all be grouped together under the 'non-ogl' facet), we index on a field
    that doesn't exist on the dataset itself.  See `SearchPlugin.before_index`.

    Another thing that DGU does differently is that it cleans up the resource
    formats prior to indexing.

    A further thing that DGU does differently is to index the group title, as
    well as the group name.
    """

    implements(IPackageController)

    def read(self, entity):
        pass

    def create(self, entity):
        pass

    def edit(self, entity):
        pass

    def authz_add_role(self, object_role):
        pass
    
    def authz_remove_role(self, object_role):
        pass

    def delete(self, entity):
        pass

    def before_search(self, search_params):
        return search_params

    def after_search(self, search_results, search_params):
        return search_results

    def before_index(self, pkg_dict):
        """
        Dynamically creates a license_id-is-ogl field to index on, and clean
        up resource formats prior to indexing.
        """
        from ckan.model.group import Group

        # Dynamically create the license_id-is-ogl field.
        if not pkg_dict.has_key('license_id-is-ogl'):
            is_ogl = self._is_ogl(pkg_dict)
            pkg_dict['license_id-is-ogl'] = is_ogl
            pkg_dict['extras_license_id-is-ogl'] = is_ogl

        # Clean the resource formats prior to indexing
        pkg_dict['res_format'] = [ self._clean_format(f) for f in pkg_dict.get('res_format', []) ]

        # Populate group titles
        if not pkg_dict.has_key('group_titles'):
            pkg_dict['group_titles'] = [Group.get(g).title for g in pkg_dict['groups']]

        return pkg_dict

    _disallowed_characters = re.compile(r'[^a-z]')
    def _clean_format(self, format_string):
        if isinstance(format_string, basestring):
            return re.sub(self._disallowed_characters, '', format_string.lower())
        else:
            return format_string

    def _is_ogl(self, pkg_dict):
        """
        Returns true iff the represented dataset has an OGL license

        A dataset has an OGL license if the license_id == "uk-ogl"
        or if it's a UKLP dataset with "Open Government License" in the
        access_contraints extra field.
        """
        regex = re.compile(r'open government licen[sc]e', re.IGNORECASE)
        return pkg_dict['license_id'] == 'uk-ogl' or \
               bool(regex.search(pkg_dict.get('extras_access_constraints', '')))
