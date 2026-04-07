from fastapi import APIRouter, Depends, Response



from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistException
from app.users.auth import get_password_hash, authenticate_user,  create_access_token
from app.users.dao import UsersDAO

from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth



router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)


@router.post("/register")   
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    
    if existing_user:
        raise UserAlreadyExistException
    
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hasned_password=hashed_password)
    
    
    
@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
   user = await authenticate_user(user_data.email, user_data.password)
   
   if not user:
       raise IncorrectEmailOrPasswordException
   
   acces_token = create_access_token({"sub": str(user.id)})
   response.set_cookie("booking_acces_token", acces_token, httponly=True)
   
   return {"acces_token": acces_token}
   
   
   

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_acces_token")
    
    
    
@router.get("/me")
async def reads_users(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def reads_users_all(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.get_all()


