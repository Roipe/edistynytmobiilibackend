from typing import List

from pydantic import BaseModel


class Category(BaseModel):
    category_id: int
    category_name: str


class GetAllCategoriesRes(BaseModel):
    categories: List[Category]


class GetCategoryRes(BaseModel):
    category: Category


class AddNewCategoryReq(BaseModel):
    category_name: str


class AddNewCategoryRes(AddNewCategoryReq):
    category_id: int


class EditCategoryReq(BaseModel):
    category_name: str
