import re
from .rpyxet import rpyxet
import os

__regex = None

# TODO: Move this to rust.


def parse_url(url):
    global __regex

    if __regex is None:
        __regex = re.compile(
            # Protocol (xet, http or https)
            r'^((?P<protocol>(https?)|(xet))://)?'
            # [[user[:pw]]@domain]
            r'(((?P<user>[^:/?#]+)(:(?P<token>[^@]*))?@)?(?P<domain>[^:/?#]+\.[a-zA-Z]+)/)?'
            r'(?P<repo>[^:/?#]+/[^:/?#]+)(/$)?'         # Repo
            r'((/src/branch)?(/(?P<branch>[^:/?#]+))?'  # Branch
            r'(/(?P<path>[^?#]+))?)?'                   # Path
        )

    m = __regex.match(url)

    if m is None:
        raise ValueError("URL '%s' not in recognized format." % url)

    r = m.groupdict()

    # Clean up one thing with the repo names
    if r['repo'].endswith('.git'):
        r['repo'] = r['repo'][:-len(".git")]

    if r['branch'] is None:
        r['branch'] = "main"

    return r


def get_url_info(url, branch=None, user=None, token=None):

    r = parse_url(url)

    xp = rpyxet.XETPath()

    domain = r.get('domain', None)
    xp.domain = domain if domain is not None else "xethub.com"

    xp.repo = r['repo']

    _branch = r.get('branch', None)
    xp.branch = branch if branch is not None else _branch

    xp.path = r.get('path', None)

    _user = r.get('user', user)
    xp.user = _user if user is None else user

    _token = r.get('token', token)
    xp.token = _token if token is None else token

    if xp.user is None:
        from .file_system import env_login_user
        xp.user = env_login_user()

    if xp.token is None:
        from .file_system import env_login_token
        xp.token = env_login_token()

    return xp
