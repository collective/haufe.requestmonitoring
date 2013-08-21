#       $Id: __init__.py,v 1.1.1.1 2005-03-04 10:46:51 dieter Exp $
'''Handler for use as request monitors.'''

import os
import Zope2

path = os.path.split(Zope2.__file__)
version_path = os.path.join(path[0], 'version.txt')
version_file = open(version_path)
version = version_file.read()

if 'Zope 2.10' in version:
    import patch
