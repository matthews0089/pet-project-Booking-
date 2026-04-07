from datetime import datetime, timezone
from jose import jwt, JWTError

from fastapi import Depends, Request


from app.config  import settings
from app.exceptions import ExpiredTokenException, JWTIssue, TokenAbsent, User_ID_Exception
from app.users.dao import UsersDAO
from app.users.models import Users



def get_token(request: Request):
    token = request.cookies.get("booking_acces_token")
    
    if not token:
        raise TokenAbsent
    
    return token


async def get_current_user(token: str = Depends(get_token)):
    
    try:
        payload =jwt.decode(
        token, 
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    
    except JWTError:
        raise JWTIssue
        
        
    expire: str = payload.get("exp")
    
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise ExpiredTokenException
    
    user_id = payload.get("sub")
    
    if not user_id:
        raise User_ID_Exception
    
    user = await UsersDAO.find_by_id(int(user_id))
    
    if not user:
        raise User_ID_Exception
    
    
    return user



async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    #if current_user.role != "admin":
        #raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user