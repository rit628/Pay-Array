import hashlib
import jwt
import os
import datetime
import re
from .orm import User

PASSWORD_ENCRYPTION_ALGORITHM = "sha256"
JWT_ENCODING_ALGORITHM = "HS256"
JWT_KEY = os.environ.get("JSON_WEB_TOKEN_KEY")
JWT_EXPIRE_MINUTES = 30
JWT_LEEWAY_SECONDS = 10

# user data regex
field_pattern_map = {
    "username" : re.compile(R"^\w{6,50}$"),
    "email" : re.compile(R"^[A-Za-z0-9._]{2,}@[A-Za-z0-9~]+\.([A-Za-z0-9-]+\.)*[a-z]{2,}$"),
    "password": re.compile(R"^[^\s]{8,}$"),
    "first_name" : re.compile(R"^[A-Za-z]+$"),
    "last_name" : re.compile(R"^[A-Za-z]+$"),
    "phone" : re.compile(R"^(\(\d{3}\)|\d{3})-?(\d{3})-?(\d{4})$")
}

class InvalidFieldError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message
    
class AuthenticationError(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message

def validate_user_data(user_data:dict) -> None:
    """Validates user data against regex patterns for each field.
       Cleans any acceptable non-standard fields to be compatible with database operations.

    Args:
        user_data (dict): User data to be validated.

    Raises:
        InvalidFieldError: Can be caught by InvalidFieldError handler in server. Contains a 400 error code.
    """
    for field, value in user_data.items():
        if not field_pattern_map[field].match(value):
            raise InvalidFieldError(f"Invalid {field}.")
        
        if field == "phone":
            phone_match = field_pattern_map["phone"].search(user_data["phone"])
            number = f"{phone_match.group(1)}{phone_match.group(2)}{phone_match.group(3)}"
            user_data["phone"] = number

def hash_password(password:str, salt:bytes = None, algorithm:str = PASSWORD_ENCRYPTION_ALGORITHM, num_iters:int = 1_000_000) -> tuple[bytes, bytes]:
    """Hashes and salts the user provided password

    Args:
        password (str): User provided password
        salt (bytes, optional): Optional explicitly provided salt, generated randomly otherwise. Defaults to None.
        algorithm (str, optional): Optional encryption algorithm. Defaults to PASSWORD_ENCRYPTION_ALGORITHM.
        num_iters (int, optional): Number of iterations to run pbkdf2_hmac hashing algorithm. Defaults to 1_000_000.

    Returns:
        tuple[bytes, bytes]: Tuple containing the encrypted password and salt, in that order.
    """
    salt = os.urandom(32) if salt is None else salt
    password_hash = hashlib.pbkdf2_hmac(algorithm, password.encode(), salt, num_iters)
    return password_hash, salt

def authenticate_user(user:User, password:str, jwt_encoding_algorithm:str = JWT_ENCODING_ALGORITHM) -> str:
    """Authenticates a user based on the provided user object and password
        and returns a JSON web token to authenticate subsequent requests.

    Args:
        user (User): A User object corresponding to the user being authenticated.
        password (str): User provided password.
        jwt_encoding_algorithm (str, optional): Encoding algorithm for JSON web token generation. Defaults to JWT_ENCODING_ALGORITHM.

    Raises:
        AuthenticationError: Can be caught by the AuthenticationError handler in the server. Contains a 401 error code.

    Returns:
        str: Generated JSON web token.
    """
    provided_hash, _ = hash_password(password, user.salt)
    if user.password_hash != provided_hash:
        raise AuthenticationError("Incorrect Password.")
    payload = {"user_id" : user.id}
    payload.update({"exp" : datetime.datetime.now() + datetime.timedelta(minutes=JWT_EXPIRE_MINUTES)})
    token = jwt.encode(payload, JWT_KEY, jwt_encoding_algorithm)
    return token

def decode_token(token:str, jwt_encoding_algorithm:str = JWT_ENCODING_ALGORITHM) -> dict:
    """Decodes the provided JSON web token.

    Args:
        token (str): JSON web token to decode.
        jwt_encoding_algorithm (str, optional): Encoding algorithm used to encode the provided token. Defaults to JWT_ENCODING_ALGORITHM.

    Raises:
        AuthenticationError: Can be caught by the AuthenticationError handler in the server. Contains a 401 error code.

    Returns:
        dict: Returns a dict with the decoded JWT payload if decode is successful."
    """
    try:
        payload = jwt.decode(token, JWT_KEY, jwt_encoding_algorithm, leeway=datetime.timedelta(seconds=JWT_LEEWAY_SECONDS))
        return payload
    except jwt.ExpiredSignatureError: # token has expired
        raise AuthenticationError("Expired Token.")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid Token.")