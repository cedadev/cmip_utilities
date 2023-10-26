
import os
import os.path
import yaml

HOME = os.environ.get('HOME')
HERE = os.path.dirname(__file__)
def user_config():
  if os.path.isdir( os.path.join( HOME, '.config' ) ):
    CMIP_UTIL_DEFAULT_CONFIG_DIR = os.path.join(HOME, '.config/cmip_utilities' )
  else:
    CMIP_UTIL_DEFAULT_CONFIG_DIR = os.path.join(HOME, '.cmip_utilities' )
  return CMIP_UTIL_DEFAULT_CONFIG_DIR

## user configuration is the only option at present
CMIP_UTIL_DEFAULT_CONFIG_DIR = user_config()
if not os.path.isdir( CMIP_UTIL_DEFAULT_CONFIG_DIR ):
    os.mkdir( CMIP_UTIL_DEFAULT_CONFIG_DIR )

CMIP_UTIL_CONFIG_DIR = os.environ.get('CMIP_UTIL_CONFIG_DIR', CMIP_UTIL_DEFAULT_CONFIG_DIR)

if not os.path.isfile( os.path.join( CMIP_UTIL_CONFIG_DIR, 'local_configuration.yml' ) ):
   os.popen( "cp %s %s" % (os.path.join( HERE, 'local_configuration.yml' ),CMIP_UTIL_CONFIG_DIR ) )
   print ( "local_configuration copied to %s" % CMIP_UTIL_CONFIG_DIR )

CONFIG_FILE = os.path.join(CMIP_UTIL_CONFIG_DIR, 'local_configuration.yml')

assert os.path.isfile( CONFIG_FILE ), '%s not found' % CONFIG_FILE

config = yaml.safe_load( open(CONFIG_FILE) )


assert 'directories' in config.keys(), 'directories entry not found in %s' % CONFIG_FILE
assert 'cmip6_cvs' in config['directories'].keys(), 'cmip6 cvs entry not found in %s' % CONFIG_FILE
