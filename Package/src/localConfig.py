
import os
import os.path

HOME = os.environ.get('HOME')
def user_config():
  if os.path.isdir( os.path.join( HOME, '.config' ):
    CMIP_UTIL_DEFAULT_CONFIG_DIR = op.join(HOME, '.config/cmip_utilities' )
  else:
    CMIP_UTIL_DEFAULT_CONFIG_DIR = op.join(HOME, '.cmip_utilities' )
  return CMIP_UTIL_DEFAULT_CONFIG_DIR


## user configuration is the only option at present
CMIP_UTIL_DEFAULT_CONFIG_DIR = user_config()

CMIP_UTIL_CONFIG_DIR = os.environ.get('CMIP_UTIL_CONFIG_DIR', CMIP_UTIL_DEFAULT_CONFIG_DIR)

