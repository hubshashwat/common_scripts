"""
Tar a folder kept in sftp and save to local
"""
import os
import tarfile
from logging import getLogger

import fsspec
from fsspec.implementations.sftp import SFTPFileSystem

import backoff as backoff
from paramiko.sftp import SFTPError

MAX_ATTEMPTS = 3
MAX_TIME = 30
REMOTE_DIR = "/data/test"
LOCAL_DIR = "download"
LOCAL_TAR_DIR = "tar"
HOST = ''
PORT = 22
USERNAME = ''
PASSWORD = ''


class DownloadTarAndSaveToLocal:
    """
    Tar a folder kept in sftp and save to local
    """

    def __init__(self, logger=getLogger(__name__)):
        self.logger = logger

    def get_sftp_fs(self,
                    host: str,
                    port: int,
                    username: str,
                    password: str = None,
                    ) -> SFTPFileSystem:
        """
        Returns a fsspec filesystem object for SFTP.
        """
        authentication_kwargs = dict()
        if password:
            authentication_kwargs["password"] = password
        return fsspec.filesystem("sftp", host=host, port=port, username=username, **authentication_kwargs)

    @backoff.on_exception(backoff.expo, SFTPError, max_tries=MAX_ATTEMPTS, max_time=MAX_TIME)
    def _download_files(self, sftp, remotedir, localdir):
        self.logger.info(f"Files available in the remote dir: {sftp.listdir(remotedir)}")
        for entry in sftp.listdir(remotedir):
            self.logger.info(f"File processing from the remote dir: {entry}")
            remotepath = entry["name"]
            localpath = os.path.join(localdir, entry["name"].split("/")[-1])
            mode = entry["type"]
            if mode == "file":
                sftp.get(remotepath, localpath)
            elif mode == "directory":
                try:
                    os.mkdir(localpath)
                except OSError:
                    pass
                self._download_files(sftp, remotepath, localpath)

    def convert_folder_to_tar(self, path):
        with tarfile.open(LOCAL_TAR_DIR + "/" + path.replace("/", "_") + "_tarfile.tar.gz", mode="w|gz") as tar:
            arcname = os.path.basename(path)  # keep path relative (optional)
            tar.add(path, arcname=arcname)

    def run(self):
        self.logger.info(f"Connecting to sftp:")
        sftp_fs = self.get_sftp_fs(host=HOST, port=PORT, username=USERNAME,
                                   password=PASSWORD)
        self.logger.info(f"Obtained a fsspec filesystem object for SFTP")
        if not os.path.exists(LOCAL_DIR):
            os.mkdir(LOCAL_DIR)
        if not os.path.exists(LOCAL_TAR_DIR):
            os.mkdir(LOCAL_TAR_DIR)
        self._download_files(sftp_fs, REMOTE_DIR, LOCAL_DIR)
        for folder in os.listdir(LOCAL_DIR):
            self.logger.info(f"Converting the folder {folder} in {LOCAL_DIR} to tar")
            self.convert_folder_to_tar(LOCAL_DIR + "/" + folder)


if __name__ == '__main__':
    """
    Update the GLOBAL variables and run the code
    """
    obj = DownloadTarAndSaveToLocal()
    obj.run()
