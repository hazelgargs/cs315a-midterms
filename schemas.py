from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class CategoryCreate(BaseModel):
  name: str
  description: Optional[str] = None


class CategoryResponse(CategoryCreate):
  id: int

model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
  title: str
  isbn: str
  publication_year: Optional[int] = None
  stock_quantity: int = Field(default=1, ge=0)
  category_id: int


class BookResponse(BookCreate):
  id: int

  model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
  title: Optional[str] = None
  isbn: Optional[str] = None
  publication_year: Optional[int] = None
  stock_quantity: Optional[int] = Field(default=None, ge=0)
  category_id: Optional[int] = None
