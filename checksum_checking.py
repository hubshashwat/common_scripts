import hashlib

sha256_checksum_1 = hashlib.sha256()
sha256_checksum_2 = hashlib.sha256()

path1 = 'test_checksum.txt'
path2 = 'ddd.py'

with open(path1, "rb") as f:
    sha256_checksum_1.update(f.read())
with open(path2, "rb") as f:
    sha256_checksum_2.update(f.read())

if sha256_checksum_1.hexdigest() == sha256_checksum_2.hexdigest():
    print('same')
else:
    print('not same')
