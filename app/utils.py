import random
import string
from datetime import datetime
from typing import Tuple
import hashlib

import os


def generate_random_string() -> Tuple[str, datetime]:
    """Gennerate a random string based appended with current datetime.

    Returns:
        Tuple[str, datetime]: The generated random string + current datetime
    """

    random_string = "".join(
        random.sample(string.ascii_letters + string.digits, 14)
    )

    current_datetime = datetime.now()
    random_string += current_datetime.strftime("%Y%m%d%H%M%S")

    return random_string, current_datetime


def generate_security_hash(seed: str) -> str:
    """Generate a security hash for verifying chat requests

    Args:
        seed (str): Seed use for generating hash (e.g. conversation ID)

    Returns:
        str: Result of sha256 hash
    """
    raise ValueError("oh lawd")

    salt = os.getenv("ADMIN_HASH")
    if not salt:
        raise Exception("ADMIN_HASH env var not set")
    admin_hash = hashlib.sha256()
    admin_hash.update(bytes(salt, "utf-8"))
    admin_hash.update(bytes(seed, "utf-8"))
    return admin_hash.hexdigest()
