import fsspec
from .url_parsing import get_url_info
from .file_interface import XetFile
from .rpyxet import rpyxet
from .commit_transaction import CommitTransaction

import os

LOGIN = "XET_USER"
TOKEN = "XET_TOKEN"


def env_login_user():
    return os.environ.get(LOGIN, None)


def env_login_token():
    return os.environ.get(TOKEN, None)


def login(user, token):
    """
    Sets XET_USER and XET_TOKEN environment variables.

    These environment variables are used to authenticate with XetHub. 
    For more information, go here: https://xethub.com/user/settings/pat
    """
    os.environ[LOGIN] = user
    os.environ[TOKEN] = token


def open(file_url, branch=None, user=None, token=None, **kwargs):
    """
    Connects to the repo given at `repo` with login info and branch `branch`.

    Returns an initialized file system handle that interfaces to the remote repo.
    TODO: Fill docs. 

    """

    fs = XetFS(file_url, branch, user, token)
    return fs.open(file_url, **kwargs)


class XetFS(fsspec.spec.AbstractFileSystem):
    protocol = "xet"  # This allows pandas, etc. to implement "xet://"
    # Whether instances can be recycled; likely possible when we figure out conflicts.

    cachable = False  # We do our own caching.
    sep = "/"
    async_impl = False
    root_marker = "/"

    # This is the repo
    _pyrepo_cache = {}

    def __init__(self, repo_url, branch=None, user=None, token=None):

        if isinstance(repo_url, rpyxet.XETPath):
            self._repo_info = repo_url
        elif isinstance(repo_url, str):
            self._repo_info = get_url_info(repo_url, branch, user, token)
        else:
            raise ValueError("Unrecognized format for given url info.")

        # Get the correct base information.
        # See if we can recycle the handle or not

        key = (self._repo_info.repo_url(),
               self._repo_info.branch, self._repo_info.user)

        try:
            self._repo_handle = self._pyrepo_cache[key]
        except KeyError:
            self._repo_handle = rpyxet.PyRepo(self._repo_info)
            self.__class__._pyrepo_cache[key] = self._repo_handle

        self._intrans = False

        # Init the base class.
        super().__init__()

    def _info_from_url(self, path):
        try:
            print("Attempting to parse url path of ", path)
            url_path = get_url_info(path)

            if self._repo_info.repo != url_path.repo:
                raise ValueError("Repo mismatch.")

        except ValueError:
            print("Using path in repo of ", path)
            url_path = self._repo_info.with_path(path)

        return url_path

    @classmethod
    def _strip_protocol(cls, path):
        """Turn path from fully-qualified to file-system-specific
        May require FS-specific handling, e.g., for relative paths or links.
        """

        if isinstance(path, list):
            return [cls._strip_protocol(p) for p in path]

        try:
            print("Attempting to parse url path of ", path)
            path = get_url_info(path).path
        except ValueError:
            print("Using the bare path of ", path)

        # use of root_marker to make minimum required path, e.g., "/"
        return path or cls.root_marker

    def unstrip_protocol(self, name):
        """Format FS-specific path to generic, including protocol"""
        self._repo_info.with_path(name)

    @staticmethod
    def _get_kwargs_from_urls(path):
        """If kwargs can be encoded in the paths, extract them here
        This should happen before instantiation of the class; incoming paths
        then should be amended to strip the options in methods.
        Examples may look like an sftp path "sftp://user@host:/my/path", where
        the user and host should become kwargs and later get stripped.
        """
        # by default, nothing happens
        return {"repo_url": path}

    @classmethod
    def current(cls):
        """Return the most recently instantiated FileSystem
        If no instance has been created, then create one with defaults
        """
        if cls._latest in cls._cache:
            return cls._cache[cls._latest]
        return cls()

    def info(self, url):
        file_url = self._info_from_url(url)
        attr = self._repo_handle.stat(file_url.branch, file_url.path)
        return {"name": file_url.path, "size": attr.size, "type": attr.ftype}

    def ls(self, path, detail=True, **kwargs):
        """List objects at path.
        This should include subdirectories and files at that location. The
        difference between a file and a directory must be clear when details
        are requested.
        The specific keys, or perhaps a FileInfo class, or similar, is TBD,
        but must be consistent across implementations.
        Must include:
        - full path to the entry (without protocol)
        - size of the entry, in bytes. If the value cannot be determined, will
          be ``None``.
        - type of entry, "file", "directory" or other
        Additional information
        may be present, appropriate to the file-system, e.g., generation,
        checksum, etc.
        May use refresh=True|False to allow use of self._ls_from_cache to
        check for a saved listing and avoid calling the backend. This would be
        common where listing may be expensive.
        Parameters
        ----------
        path: str
        detail: bool
            if True, gives a list of dictionaries, where each is the same as
            the result of ``info(path)``. If False, gives a list of paths
            (str).
        kwargs: may have additional backend-specific options, such as version
            information
        Returns
        -------
        List of strings if detail is False, or list of directory information
        dicts if detail is True.  These dicts would have: name (full path in the FS), 
        size (in bytes), type (file, directory, or something else) and other FS-specific keys.
        """
        url_path = self._info_from_url(path)
        files, file_info = self._repo_handle.readdir(url_path)
        if url_path.path and url_path.path != '/':
            files = [(os.path.join(url_path.path, fname)) for fname in files]

        if detail:
            return [{"name": fname, "size": finfo.size, "type": finfo.ftype}
                    for fname, finfo in zip(files, file_info)]
        else:
            return files

    def _open(
        self,
        path,
        mode="rb",
        **kwargs,
    ):
        """Return raw bytes-mode file-like from the file-system"""

        transaction = getattr(self, "_transaction", None)

        if transaction is None and not mode.startswith('r'):
            raise RuntimeError(
                "Write access to files is only allowed within a commit transaction.")

        if not mode.startswith('r'):
            if not self._intrans:
                raise RuntimeError("Write only allowed in the context of a commit transaction."
                                   "Use `with fs.commit(...):` to enable write access.")

        branch = self._repo_info.branch

        if mode.startswith('r'):
            handle = self._repo_handle.open_for_read(branch, path)
        elif mode.startswith('a'):
            handle = self._repo_handle.open_for_write(branch, path, True)
        elif mode.startswith('w'):
            handle = self._repo_handle.open_for_write(branch, path, False)
        else:
            raise ValueError("Mode '%s' not supported.", mode)

        return XetFile(
            self,
            handle,
            path,
            mode,
            **kwargs,
        )

    def rm(self, path):
        """Delete a file"""
        raise NotImplementedError

    def cp_file(self, path1, path2, **kwargs):
        raise NotImplementedError

    @property
    def transaction(self):
        """A context within which files are committed together upon exit
        Requires the file class to implement `.commit()` and `.discard()`
        for the normal and exception cases.
        """
        raise NotImplementedError

    def start_transaction(self):
        """Begin write transaction for deferring files, non-context version"""

        raise NotImplementedError
        if self._intrans:
            raise RuntimeError("Commit transaction already in progress.")

        self._intrans = True
        self._transaction = CommitTransaction(self, None)

        return self.transaction

    def end_transaction(self):
        """Finish write transaction, non-context version"""
        raise NotImplementedError
        self._transaction.complete()
        self._transaction = None
        self._intrans = False


fsspec.register_implementation("xet", XetFS, clobber=True)
