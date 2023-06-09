from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    full_name: str
    password: str


class ChangePass(BaseModel):
    password: str


class User(UserBase):
    id: int
    username: str
    full_name: str
    disabled: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str
