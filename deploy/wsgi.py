
import os
import sys
import site


def prepend_package_paths(directories):
    """
    Add given paths to 'sys.path'

    Uses site.addsitedir() so that '.pth' files are processed correctly, but
    unlike that function, this one takes care to add the custom paths to the
    front of sys.path to ensure they take precedence.

    http://code.google.com/p/modwsgi/wiki/VirtualEnvironments
    """
    # Remember original sys.path.
    prev_sys_path = list(sys.path)

    # Add each new site-packages directory.
    for directory in directories:
        site.addsitedir(directory)

    # Reorder sys.path so new directories at the front.
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path


# Add our python-virtualenv and Django project to sys.path
paths = (
    '/usr/local/lib/python2.7/dist-packages',
    '/var/www/tepromark.com/source',)
prepend_package_paths(paths)

# Create Django's WSGI application
import django.core.handlers.wsgi
os.environ['DJANGO_SETTINGS_MODULE'] = 'common.settings.development'
application = django.core.handlers.wsgi.WSGIHandler()

