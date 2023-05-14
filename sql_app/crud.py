from sqlalchemy.orm import Session
from . import models, schemas

# USER
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, payload: schemas.UserUpdate, user_id: int):
    user_query = db.query(models.User).filter(models.User.id==user_id)
    user = user_query.first()
    update_user = payload.dict(exclude_unset=True)
    user_query.filter(models.User.id==user_id).update(update_user, synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id:int):
    user_query = db.query(models.User).filter(models.User.id==user_id)
    user = user_query.first()
    user_query.delete(synchronize_session=False)
    # delete todos associated with user
    todo_query = db.query(models.Todo).filter(models.Todo.user_id==user_id)
    todo_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "user deleted successfully"}


# TODO
def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()


def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, payload: schemas.TodoUpdate, todo_id: int):
    todo_query = db.query(models.Todo).filter(models.Todo.id==todo_id)
    todo = todo_query.first()
    update_todo = payload.dict(exclude_unset=True)
    todo_query.filter(models.Todo.id==todo_id).update(update_todo, synchronize_session=False)
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id:int):
    todo_query = db.query(models.Todo).filter(models.Todo.id==todo_id)
    todo = todo_query.first()
    todo_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "todo deleted successfully"}