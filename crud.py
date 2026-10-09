import models
import schemas
from sqlalchemy.orm import Session


def create_category(db: Session, category: schemas.CategoryCreate):
  db_category = models.Category(**category.model_dump())
  db.add(db_category)
  db.commit()
  db.refresh(db_category)
  return db_category

def get_categories(db: Session):
  return db.query(models.Category).all()
  

def create_book(db: Session, book: schemas.BookCreate):
  db_book = models.Book(**book.model_dump())
  db.add(db_book)
  db.commit()
  db.refresh(db_book)
  return db_book


def get_books(db: Session, category_id=None):
  query = db.query(models.Book)

  if category_id is not None:
    query = query.filter(models.Book.category_id == category_id)

  return query.all()


def get_book(db: Session, book_id: int):
  return db.query(models.Book).filter(
    models.Book.id == book_id
).first()


def update_book(db: Session, book_id: int, book_data: schemas.BookUpdate):
  db_book = get_book(db, book_id)

  if db_book is None:
    return None

  updates = book_data.model_dump(exclude_unset=True)

  for key, value in updates.items():
    setattr(db_book, key, value)

  db.commit()
  db.refresh(db_book)  
  return db_book


def delete_book(db: Session, book_id: int):
  db_book = get_book(db, book_id)

  if db_book is None:
    return None

  db.delete(db_book)
  db.commit()
  return db_book
