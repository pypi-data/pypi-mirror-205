import fsspec


class CommitTransaction(fsspec.transaction.Transaction):
    """
    A commit implementing the transaction interface to allow atomic commits.

    A commit gets created and pushed on transaction completion. 

    See
    https://github.com/fsspec/filesystem_spec/blob/master/fsspec/transaction.py

    """

    def __init__(self, fs, commit_message=None):
        if commit_message is None:
            import datetime
            commit_message = "Commit " + datetime.datetime.now().isoformat()

        self.commit_message = commit_message
        self.fs = fs

        super().__init__(fs)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End transaction and commit, if exit is not due to exception"""
        # only commit if there was no exception
        self.complete(commit=exc_type is None)
        self.fs._intrans = False
        self.fs._transaction = None

    def start(self):
        self.fs._intrans = True

    def complete(self, commit=True):

        if commit:
            self.fs._repo_handle.commit_and_push_current(
                self.fs._repo_info.branch, self.commit_message)
        else:
            self.fs._repo_handle.reset(self.fs._repo_info.branch)

        self.fs._intrans = False
        self.fs._transaction = None
