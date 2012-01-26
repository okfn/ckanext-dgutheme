import os

from logging import getLogger

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, IRoutes
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

