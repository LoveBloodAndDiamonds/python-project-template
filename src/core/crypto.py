__all__ = ["Cryptography"]

from base64 import b64decode, b64encode
from hashlib import sha256

from Crypto.Cipher import AES


class Cryptography:
    """Вспомогательный класс для шифрования данных."""

    def __init__(self, secret: str) -> None:
        """Инициализирует объект класса Cryptography.

        Args:
            secret: Секретный ключ для шифрования.

        """
        self.key = sha256(secret.encode()).digest()

    def encrypt(self, data: str) -> str:
        """Шифрует данные с использованием AES.

        Args:
            data: Строка для шифрования.

        Returns:
            Base64-строка, содержащая nonce, тег и зашифрованные данные.

        """
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Расшифровывает данные, зашифрованные с использованием AES.

        Args:
            encrypted_data: Base64-строка, полученная из метода encrypt.

        Returns:
            Исходная расшифрованная строка.

        """
        raw_data = b64decode(encrypted_data)
        nonce, tag, ciphertext = raw_data[:16], raw_data[16:32], raw_data[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
