import re
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

@staticmethod
def url_safe_value(value: str) -> str:
    '''
        Make a text string URL-safe by converting it to lowercase, replacing spaces with hyphens, and removing non-alphanumeric characters.
        Args:
            value (str): The text string to make URL-safe.
        returns:
            str: The URL-safe version of the input string.
    '''
    # Convert to lowercase, replace spaces with hyphens, remove non-alphanumeric characters
    return re.sub(r'[^a-z0-9-]', '', value.lower().replace(' ', '-'))