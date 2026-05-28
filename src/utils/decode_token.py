from jose import JWTError, jwt
from src.config.settings import settings    
from src.core.exception.custom_exception import (
    UnauthorizedException,
) 
import logging
logger = logging.getLogger(__name__) 
# if jwt.decode sucess it return dict otherwise it raises exeception

def decode_token(token: str) -> dict:
        """Decode and validate a JWT token. Returns None if invalid."""
        try:
            return jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            raise UnauthorizedException("Token expired")
        except JWTError:
            logger.warning("Invalid token")
            raise UnauthorizedException("invalid token")