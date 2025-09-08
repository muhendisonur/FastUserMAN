# user_routes.py
from typing import Annotated, List, Union
from fastapi import APIRouter, Depends, HTTPException, status

from services.user_service import UserService
from schemas.User import User
from schemas.UserUpdate import UserUpdate
from schemas.UserWithoutID import UserWithoutID
from config import db_path, url_prefix

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


user_router = APIRouter(
    prefix=url_prefix,
    tags=[url_prefix]
)

engine = create_engine(f"sqlite:///{db_path}", echo=True)
Session = sessionmaker(bind=engine)

def get_session():
    try:
        session = Session()
        yield UserService(session)
    finally:
        session.close()

service_di = Annotated[UserService, Depends(get_session)]

@user_router.get("/", response_model=Union[List[User], None])
async def all_users(service: service_di):
    """
        Returns all users

        Returns:
            object(List[User]): schemas.User data type objects in a List
    """
    return service.get_users()


# Endpoint'i bu standart formatta tanımla
@user_router.get("/{user_id}", response_model=User)
async def user_by_id(user_id: int, service: service_di):
    """
    Finds a user by their ID.

    Args:
        user_id: user_id of user's to be presented

    Returns:
        db_user (dict): returns user data dictionary
    """
    try:
        found_user = service.get_user_by_id(user_id)
        
        if found_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
            
        return found_user
    except ValueError:
        raise ValueError("user_id must be integer!")

@user_router.get("/delete/{user_id}")
async def remove_user_by_id(user_id: int, service: service_di):
    """
        Deletes an user from the database by user_id

        Args:
            user_id: user_id of user's to be deleted

        Returns:
            object (dict): contains message key with a value that describe the situation
    """
    is_removed = service.remove_user_by_id(user_id)
    if is_removed:
        return {"detail:": f"user with {user_id} id has been deleted!"}
    else:
        raise HTTPException(status_code=404, detail=f"user with {user_id} id not found!")
    
@user_router.post("/add")
async def add_user(user_create: UserWithoutID, service: service_di):
    """
        Adds user into the database

        Args:
            user_create (Pydantic.BaseModel): this object have user's field without user_id field

        Returns:
            object (dict): contains detail key with a value that describe the situation
    """
    is_succ = service.insert_user(
        user_create.name, 
        user_create.email, 
        user_create.age
        )
    if is_succ:
        return {"detail": "user added succesfully!"}
    else:
        raise HTTPException(status_code=422, detail="user couldnt insert into database!")
    
@user_router.put("/update")
async def update_user(user_update: UserUpdate, service: service_di):
    is_succ = service.update_user_by_id(user_update.__repr__()) # service wants param as dict so with repr attribute, we convert the object into dict
    if not is_succ:
        HTTPException(status_code=500, detail="An error occured while is updating the user")
    return {"detail": "user has been updated!"}
