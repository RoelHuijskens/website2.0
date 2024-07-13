import random
import string
from datetime import datetime
from typing import Tuple
import hashlib

import os

def generate_random_string() -> Tuple[str, datetime]:
    # Generate random string with 14 unique characters
    random_string = ''.join(random.sample(string.ascii_letters + string.digits, 14))
    
    # Append current datetime as a string
    current_datetime = datetime.now()
    random_string += current_datetime.strftime("%Y%m%d%H%M%S")
    
    return random_string, current_datetime


def generate_security_hash(seed:str) -> str:
    
    admin_hash = hashlib.sha256()
    admin_hash.update(bytes(os.getenv("ADMIN_HASH"), 'utf-8'))
    admin_hash.update(bytes(seed, 'utf-8'))
    return admin_hash.hexdigest()