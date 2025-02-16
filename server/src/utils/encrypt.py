from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify if a password is correct.

    Parameters
    ----------
    password : str
        Password to be verified.
    hashed_password : str
        Hashed password.
    """
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get the hash of a password.

    Parameters
    ----------
    password : str
        Password to be hashed.
    """
    return pwd_context.hash(password)
