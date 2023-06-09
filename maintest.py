import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print("helloo")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
    # return {"email": "nvthuong@cmcglobal.vn", "is_active": True}


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.ChangePass, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    # use setattr(data, file, value) to update
    setattr(db_user, "hashed_password", user.password)
    db.add(db_user)
    # put data in db
    db.commit()
    db.refresh(db_user)
    return "Successfully!"


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    db.delete(db_user)
    db.commit()
    return "Delete Successfully!"


@app.get("/users/search/{email}")
def search_user_by_email(email: str, db: Session = Depends(get_db)):
    data = crud.search_user_by_email(db=db, email=email)
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return data


if __name__ == "__main__":
    uvicorn.run('main:app', port=8080, log_level='info', reload=True)
