import random
import string


class Password:
    @staticmethod
    def generate() -> str:
        """Generate a new password."""
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(10))
        return password