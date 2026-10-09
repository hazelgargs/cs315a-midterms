from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


# 1. create category
@app.post("/categories/", response_model=schemas.CategoryResponse, status_code=201)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(models.Category).filter(
        models.Category.name == category.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category name already exists"
        )

    new_category = models.Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# 2. get all categories
@app.get("/categories/", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


# 3. create book
@app.post("/books/", response_model=schemas.BookResponse, status_code=201)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    category = db.query(models.Category).filter(
        models.Category.id == book.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category does not exist"
        )

    existing = db.query(models.Book).filter(
        models.Book.isbn == book.isbn
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )

    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# 4. get all books with optional category filter
@app.get("/books/", response_model=list[schemas.BookResponse])
def get_books(
    category_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)

    if category_id is not None:
        category = db.query(models.Category).filter(
            models.Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        query = query.filter(
            models.Book.category_id == category_id
        )

    return query.all()


# 5. get one book by ID
@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
  book = db.query(models.Book).filter(
    models.Book.id == book_id
  ).first()

  if not book:
    raise HTTPException(
      status_code=404,
      detail="Book not found"
    )

  return book