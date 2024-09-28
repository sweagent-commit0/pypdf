import secrets
from Crypto import __version__
from Crypto.Cipher import AES, ARC4
from Crypto.Util.Padding import pad
from pypdf._crypt_providers._base import CryptBase
crypt_provider = ('pycryptodome', __version__)

class CryptRC4(CryptBase):

    def __init__(self, key: bytes) -> None:
        self.key = key

class CryptAES(CryptBase):

    def __init__(self, key: bytes) -> None:
        self.key = key