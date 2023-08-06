import fsspec
import io


class XetFile:
    """
    A file in a XetRepo. 

    For now, derive from AbstractBufferedFile as it only requires us to implement 
    a very small number of functions and fills in the rest.  In the future, 
    we can optimize this.

    It is possible we don't need to do the BufferedFile part

    https://github.com/fsspec/filesystem_spec/blob/master/fsspec/spec.py#L1435

    """

    def __init__(
        self,
        fs,
        handle,
        path,
        mode="rb",
        **kwargs,
    ):

        # Get pyxethandle  from path if None.
        self.handle = handle

    @property
    def closed(self):
        return self.handle.is_closed()

    def close(self):
        return self.handle.close()

    def fileno(self):
        # TODO - probably there is a better way to do this? - this is needed for open(mode='w') to work
        return self.handle.__hash__()

    def isatty(self):
        return False

    def flush(self):
        pass

    def readable(self):
        return self.handle.readable()

    def seekable(self):
        return self.handle.seekable()

    def writable(self):
        return self.handle.writable()

    def readline(self, size=-1):
        if size is None:
            return self.handle.readline(-1)
        if isinstance(size, int):
            return self.handle.readline(size)
        raise TypeError("size must be an integer")

    def readlines(self, hint=-1):
        if hint is None:
            return self.handle.readlines(-1)

        if isinstance(hint, int):
            return self.handle.readlines(hint)

        raise TypeError("hint must be an integer")

    def seek(self, offset, whence=io.SEEK_SET):
        if whence not in (io.SEEK_SET, io.SEEK_CUR, io.SEEK_END):
            raise ValueError("Unexpected value for whence")
        if not isinstance(offset, int):
            raise TypeError("Unexpected type for offset")

        return self.handle.seek(offset, whence)

    def tell(self):
        return self.handle.tell()

    def read(self, size=-1):
        if not isinstance(size, int):
            raise TypeError("Unexpected type for size")
        return self.handle.read(size)

    def readall(self):
        return self.handle.readall()

    def readinto(self, b):
        return self.handle.readinto(b)

    def readinto1(self, b):
        return self.handle.readinto1(b)

        self.handle.write(self.buffer)

    def write(self, data):
        if not self.writable():
            raise ValueError("File not in write mode")
        if self.closed:
            raise ValueError("I/O operation on closed file.")

        self.handle.write(data)

    def __del__(self):
        if not self.closed:
            self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
