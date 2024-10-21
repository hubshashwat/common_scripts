"""
brew install corkscrew
"""

import io
import logging

from paramiko import RSAKey
import fsspec
import paramiko

logging.basicConfig()
logging.getLogger("paramiko").setLevel(logging.DEBUG) # for example


def with_proxy():
    # pkey = RSAKey.from_private_key(io.StringIO(credentials['private_key_ascii']))
    pkey = paramiko.Ed25519Key.from_private_key(io.StringIO(credentials['private_key_ascii']))
    pcommand = f'corkscrew {credentials["proxy_host"]} {credentials["proxy_port"]} %s %d' % (credentials['host'], credentials['port'])
    proxy = paramiko.proxy.ProxyCommand(pcommand)

    authentication_kwargs = dict()
    authentication_kwargs["pkey"] = pkey
    authentication_kwargs["sock"] = proxy

    fs = fsspec.filesystem(
        "sftp", host=credentials['host'], port=credentials['port'], username=credentials['username'], **authentication_kwargs
    )
    if fs:
        print("fs found:")
        files = fs.ls("/", detail=True)
        print("Files in the remote directory:")
        k = []
        for file in files:
            k.append(file['name'])
        print(sorted(k))


def without_proxy():
    pkey = RSAKey.from_private_key(io.StringIO(credentials['private_key_ascii']))
    authentication_kwargs = dict()
    authentication_kwargs["pkey"] = pkey

    fs = fsspec.filesystem(
        "sftp", host=credentials['host'], port=credentials['port'], username=credentials['username'], **authentication_kwargs
    )
    if fs:
        print("fs found:")
        files = fs.ls("/", detail=True)
        print("Files in the remote directory:")
        for file in files:
            print(file['name'])


if __name__ == '__main__':
    credentials = {"host": "sftp.bloomberg.com", "port": 22, "username": "", "proxy_host": "", "proxy_port": 8080}

    with_proxy()
