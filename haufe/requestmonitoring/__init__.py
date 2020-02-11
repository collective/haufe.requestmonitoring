# -*- coding: utf-8 -*-
#       $Id: __init__.py,v 1.1.1.1 2005-03-04 10:46:51 dieter Exp $
'''Handler for use as request monitors.'''

# Zope versions > 2.11 don't need to be patched this way

from App.version_txt import getZopeVersion

major, minor, micro, status, release = getZopeVersion()

if major == 2 and minor <= 10:
    import patch  # noqa
