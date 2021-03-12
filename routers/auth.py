from models.token import Token
from config.settings import get_settings
from datetime import timedelta
from dependencies.auth import authenticate_user, create_access_token, get_current_user
from sqlalchemy.exc import IntegrityError
from repositories.users_repository import UsersRepository
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.params import Depends
from models.user import User, UserCreate

settings = get_settings()

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=User)
def register(user: UserCreate, repo: UsersRepository = Depends(UsersRepository)):
    try:
        created_user_id = repo.createUser(user)
        created_user = repo.getUserById(created_user_id)
        if (not created_user):
            raise HTTPException(
                status_code=404, detail="User was not created."
            )
        return created_user
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="Already registered.")


@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def me(current_user: User = Depends(get_current_user)):
    return current_user
