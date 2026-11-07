import argon2
from argon2.exceptions import VerifyMismatchError


class PasswordHasher:
    def __init__(self) -> None:
        self.password_hasher = argon2.PasswordHasher()

    def hash_password(self, password: str) -> str:
        hashed_password = self.password_hasher.hash(password)
        return hashed_password

    def compare(self, hashed_password: str, password: str) -> bool:
        """
        Compare hashed password with password.
        If equal, return True. Else return False.
        :param hashed_password:
        :param password:
        :return:
        """
        try:
            return self.password_hasher.verify(hashed_password, password)
        except VerifyMismatchError:
            return False
