import secrets
from cryptography import __version__
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers.algorithms import AES
try:
    from cryptography.hazmat.decrepit.ciphers.algorithms import ARC4
except ImportError:
    from cryptography.hazmat.primitives.ciphers.algorithms import ARC4
from cryptography.hazmat.primitives.ciphers.base import Cipher
from cryptography.hazmat.primitives.ciphers.modes import CBC, ECB
from pypdf._crypt_providers._base import CryptBase
crypt_provider = ('cryptography', __version__)

class CryptRC4(CryptBase):

    def __init__(self, key: bytes) -> None:
        self.cipher = Cipher(ARC4(key), mode=None)

class CryptAES(CryptBase):

    def __init__(self, key: bytes) -> None:
        self.alg = AES(key)