from database.models import User
from exceptions import UserExistsError

from typing import Union, List

from sqlalchemy import select
from sqlalchemy.orm import Session



class UserService:
    def __init__(self, session: Session):
       self.session = session

    def insert_user(self, user_add_name: str, user_add_email: str, user_add_age: int) -> bool:
        """
            Insert new user into Users table on database

            Returns:
                True/False (bool): if the process succesful returns True otherwise returns False
        """
        # checks if an user with same email address exists. If there is, returns False wtihout adding process.
        if not self.get_user_by_email(user_add_email) == None:
            raise UserExistsError
        user = User()
        user.name = user_add_name
        user.email = user_add_email
        user.age = user_add_age
        
        self.session.add(user)
        self.session.commit()
        return True
    
    def get_users(self) -> Union[List[User], None]:
        """
            Returns all the user dictionary as a list

            Returns: 
                object (list)/None: return user objects in a list, if any user couldnt find on DB returns None
        """
 
        stmt = select(User)
        users = self.session.scalars(stmt).all()
        return users if not users == [] else None # return None if the list is empty, if it's not empty return a list that contains user objects

    def get_user_by_email(self, temp_email: str) -> User:
        """
            Returns User object as dictonary by email field

            Returns:
                object (database.models.User): user object that contains data fields
        """
    
        stmt = select(User).where(User.email == temp_email)
        return self.session.execute(stmt).scalar_one_or_none() # returns User object of the user or None.

    def get_user_by_id(self, temp_id: int) -> Union[User, None]:
        """
            Returns User object as dictonary by user_id field

            Returns:
                object(User): User object that contains user's fields
        """
        return self.session.get(User, temp_id)

    def remove_user_by_id(self, temp_id: int) -> bool:
        """
            Deletes the user from database by email address

            Returns:
                True/False (bool): if the process succesful returns True otherwise returns False
        """
        stmt = select(User).where(User.user_id == temp_id)
        user = self.session.execute(stmt).scalar_one_or_none()
        if not user == None:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

        
    def update_user_by_id(self, user_update: dict) -> bool: # validation yapılmıyor pydantic kullanılarak o düzeltilecek
        """
            Updates the user of matched user id

            Args:
                user_update(sqlalchemy.orm.DeclarativeBase): contains datas that will be swapping with original

            Returns:
                object(bool): presents the situation. True means update successful. False means update unsuccessful.
        """
        stmt = select(User).where(User.user_id == user_update.get("user_id"))
        user = self.session.execute(stmt).scalar_one_or_none() # select the user to be updated 

        if user is None:
            return False
        
        for field, value in user_update.items():
            if value == None:
                continue
            setattr(user, field, value)
    
        self.session.commit()
        return True