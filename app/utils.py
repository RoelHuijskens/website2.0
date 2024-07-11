import random
import string
from datetime import datetime
from typing import Tuple

def generate_random_string() -> Tuple[str, datetime]:
    # Generate random string with 14 unique characters
    random_string = ''.join(random.sample(string.ascii_letters + string.digits, 14))
    
    # Append current datetime as a string
    current_datetime = datetime.now()
    random_string += current_datetime.strftime("%Y%m%d%H%M%S")
    
    return random_string, current_datetime