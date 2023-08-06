from .rpyxet import rpyxet
import io
import fsspec

_repo_pool = {}


def _parse_path(url, allow_empty_path=False):
    expected_path_components = 4
    if allow_empty_path:
        expected_path_components = 3

    path = ""
    if url.startswith("http://") or url.startswith("https://"):
        from urllib.parse import urlparse
        parse = urlparse(url)
        # the first path component is empty as parse.path begins with '/'
        pathsplit = parse.path.split('/')[1:]
        if len(pathsplit) < expected_path_components:
            raise ValueError("URL must be of the form"
                             "https://xethub.com/user/repo.git/branch/path")
        user = pathsplit[0]
        repo = pathsplit[1]
        branch = pathsplit[2]
        if len(pathsplit) >= 4:
            path = '/'.join(pathsplit[3:])
        remote = parse.scheme + "://" + parse.netloc
    elif url.startswith("xet@") or url.startswith("git@"):
        urlsplit = url.split(':')
        if len(urlsplit) != 2:
            raise ValueError("SSH URL must be of the form"
                             "xet@xethub.com:username/repo.git/branch/path")
        remote = urlsplit[0]  # xet@xethub.com
        pathsplit = urlsplit[1].split('/')
        if len(pathsplit) < expected_path_components:
            raise ValueError("URL must be of the form"
                             "xet@xethub.com:username/repo.git/branch/path")
        user = pathsplit[0]
        repo = pathsplit[1]
        branch = pathsplit[2]
        if len(pathsplit) >= 4:
            path = '/'.join(pathsplit[3:])
    else:
        raise ValueError("URL must be a http/https or a SSH path")

    if not repo.endswith(".git"):
        raise ValueError("Repo is expected to end with .git")

    return (remote, user, repo, branch, path)


def open(url):
    """
    Opens a xet file in a Xet repo.
    URL is a complete path of the form:
      xet@xethub.com:username/repo.git/branch/path...
    or https://xethub.com/user/repo.git/branch/path
    """
    remote, user, repo, branch, path = _parse_path(url)
    if not repo.endswith(".git"):
        raise ValueError("Repo is expected to end with .git")

    repo_key = '/'.join([remote, user, repo])
    if repo_key not in _repo_pool:
        _repo_pool[repo_key] = rpyxet.PyRepo(repo_key)

    return XetFile(_repo_pool[repo_key].open(branch, path))


def info(url):
    remote, user, repo, branch, path = _parse_path(url)
    repo_key = '/'.join([remote, user, repo])
    if repo_key not in _repo_pool:
        _repo_pool[repo_key] = rpyxet.PyRepo(repo_key)
    stat = _repo_pool[repo_key].stat(branch, path)
    return {"type": stat.ftype,
            "size": stat.size,
            "name": "/".join([repo, branch, path])}


def ls(url, detail=True):
    remote, user, repo, branch, path = _parse_path(url, True)
    repo_key = '/'.join([remote, user, repo])
    if repo_key not in _repo_pool:
        _repo_pool[repo_key] = rpyxet.PyRepo(repo_key)
    names, listing = _repo_pool[repo_key].readdir(branch, path)
    if len(path) == 0:
        prefix = "/".join([repo, branch])
    else:
        prefix = "/".join([repo, branch, path])

    if detail is False:
        return ["/".join([prefix, n]) for n in names]
    return [{"type": stat.ftype,
             "size": stat.size,
             "name": "/".join([prefix, name])}
            for (name, stat) in zip(names, listing)]
