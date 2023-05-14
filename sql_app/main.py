from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# USER
# add new user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# return all users
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# get user by id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# update user
@app.put("/users/edit/{user_id}/", response_model=schemas.User)
def edit_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    return crud.update_user(db=db, payload=user, user_id=user_id)

# delete user
@app.delete("/users/delete/{user_id}/")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)


# TODOS
# add todo for a user
@app.post("/users/{user_id}/todos/", response_model=schemas.Todo)
def create_todo_for_user(
    user_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)
):
    return crud.create_user_todo(db=db, todo=todo, user_id=user_id)

# fetch all todos
@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

# fetch all todos for a user

# update a todo
@app.put("/todos/edit/{todo_id}/", response_model=schemas.Todo)
def edit_todo(
    todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)
):
    return crud.update_todo(db=db, payload=todo, todo_id=todo_id)

# delete a todo
@app.delete("/todos/delete/{todo_id}/")
def remove_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db=db, todo_id=todo_id)
