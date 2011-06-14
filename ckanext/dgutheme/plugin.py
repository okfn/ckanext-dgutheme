import os

from logging import getLogger

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
import ckanext.dgutheme

from ckan.model import Session
from ckanext.harvest.model import HarvestObject

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
            config[config_var] += ',' + absolute_path
        else:
            config[config_var] = absolute_path


class EmbeddedThemePlugin(SingletonPlugin):
    '''DGU Visual Theme for a CKAN install embedded in dgu/Drupal.

    '''
    implements(IConfigurer)

    def update_config(self, config):
        configure_template_directory(config, 'theme_embedded/templates')
        configure_public_directory(config, 'theme_embedded/public')
        configure_template_directory(config, 'theme_common/templates')
        configure_public_directory(config, 'theme_common/public')

        config['package_form'] = 'package_gov3'


class IndependentThemePlugin(SingletonPlugin):
    '''DGU Visual Theme for a CKAN install independent of dgu/Drupal.

    '''
    implements(IConfigurer)

    def update_config(self, config):
        configure_template_directory(config, 'theme_independent/templates')
        configure_public_directory(config, 'theme_independent/public')
        configure_template_directory(config, 'theme_common/templates')
        configure_public_directory(config, 'theme_common/public')

        config['package_form'] = 'package_gov3'

class WalesThemePlugin(SingletonPlugin):
    '''DGU/Wales Visual Theme for a CKAN install independent of dgu/Drupal.

    '''
    implements(IConfigurer)

    def update_config(self, config):
        configure_template_directory(config, 'theme_wales/templates')
        configure_public_directory(config, 'theme_wales/public')
        configure_template_directory(config, 'theme_independent/templates')
        configure_public_directory(config, 'theme_independent/public')
        configure_template_directory(config, 'theme_common/templates')
        configure_public_directory(config, 'theme_common/public')

        config['package_form'] = 'package_gov3'
        if config.get('ckan.site_title') in ('CKAN', None):
            config['ckan.site_title'] = 'Data Wales'
        if not config.get('ckan.site_logo'):
            config['ckan.site_logo'] = '/images/wales.jpg'
        config['ckan.banner_logo'] = '/images/wag_logo.jpg'

