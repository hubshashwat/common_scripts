import io
import time
from datetime import timedelta
import psutil
import addict
import gnupg


def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / (1024 ** 2)


class GPGHandler:
    def __init__(self, gpg_private_ascii: str, passphrase: str):
        self.gpg_key = gnupg.GPG()
        self.passphrase = passphrase
        self.gpg_key.import_keys(gpg_private_ascii)
        try:
            self.gpg_key_id = self.gpg_key.list_keys()[-1]["keyid"]
            print(f"Using GPG_KEY_ID={self.gpg_key_id}")
        except IndexError:
            raise ValueError("No GPG key found")

    def decrypt_file_object(self, encrypted_file_object):
        encrypted_file_object.seek(0)
        result = self.gpg_key.decrypt_file(encrypted_file_object, always_trust=True, passphrase=self.passphrase)
        if not result.ok:
            raise ValueError(f"Decryption failed. KEY_ID={result.key_id}, Status - {result.status}")
        decrypted_file_object = io.BytesIO(result.data)
        decrypted_file_object.seek(0)
        return decrypted_file_object

    def encrypt_file_object(self, file_object: io.BytesIO) -> io.BytesIO:
        """
        Encrypt a file object.
        """
        encrypted_file_object = io.BytesIO()
        encrypted_file_object.write(
            self.gpg_key.encrypt(file_object.getvalue(), self.gpg_key_id, always_trust=True).data
        )
        encrypted_file_object.seek(0)
        return encrypted_file_object


if __name__ == '__main__':
    memory_before = get_memory_usage()
    print("memory before", memory_before)

    # read pgp file
    with open("13744603840.zip.pgp", "rb") as file:
        file_content = file.read()

    # add secrets
    _secrets = addict.Dict(
        {
            "gpg_private_ascii": "",
            "gpg_pubring_passphrase": ""
        }
    )

    _gpg_handler = GPGHandler(
        gpg_private_ascii=_secrets.gpg_private_ascii,
        passphrase=_secrets.gpg_pubring_passphrase,
    )
    _start = time.time()
    decrypted_content = _gpg_handler.decrypt_file_object(
        io.BytesIO(file_content),
    ).read()
    _time_taken = str(timedelta(seconds=time.time() - _start))
    print(f"[DECRYPTION-COMPLETED with READING] for file, TimeTaken: {_time_taken}")
    memory_after = get_memory_usage()
    print("memory after", memory_after)
