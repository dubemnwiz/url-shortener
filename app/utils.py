import random
import string

_ALPHABET = string.ascii_letters + string.digits
_CODE_LENGTH = 6


def generate_short_code(length: int = _CODE_LENGTH) -> str:
    """Return a random alphanumeric string of `length` characters."""
    return "".join(random.choices(_ALPHABET, k=length))


def unique_short_code(exists_fn, length: int = _CODE_LENGTH, max_attempts: int = 10) -> str:
    """Generate a short code that does not already exist in the database.

    `exists_fn` is a callable that takes a candidate code and returns True
    if that code is already taken (e.g. a DB lookup).  Raises RuntimeError
    after `max_attempts` collisions — practically impossible at normal scale
    but prevents an infinite loop in a very full namespace.
    """
    for _ in range(max_attempts):
        code = generate_short_code(length)
        if not exists_fn(code):
            return code
    raise RuntimeError(
        f"Could not generate a unique short code after {max_attempts} attempts."
    )
