import secrets
from typing import Annotated
from fastapi import  Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import status
from core.config import settings

security = HTTPBasic()

def user_authorized(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """
    Verifica se as credenciais de usuário são válidas.

    Args:
        credentials (HTTPBasicCredentials): As credenciais de autenticação.

    Returns:
        str: O nome de usuário, se as credenciais forem válidas.

    Raises:
        HTTPException: Se as credenciais forem inválidas.
    """
    
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = settings.ROUTER_LOGIN.encode("utf8")
    is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = settings.ROUTER_PWD.encode("utf8")
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
