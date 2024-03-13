import datetime
import uuid
from typing import Annotated

from fastapi import Depends, HTTPException

import models
# import models_old
from dependencies import LoggedInUser
from dtos.category import EditCategoryReq
from dtos.rental_item import AddItemToCategoryReq
from services.base import BaseService


class CategoryService(BaseService):
    def __init__(self, db: models.Db):
        super(CategoryService, self).__init__(db)

    def get_all(self):
        return self.db.query(models.Category).all()

    def create(self, category: models.Category):
        self.db.add(category)
        self.db.commit()

    def get_category_by_id(self, _id: int):
        return self.db.query(models.Category).filter(models.Category.category_id == _id).first()

    def remove(self, _id: int):
        cat = self.get_category_by_id(_id)
        if cat is None:
            raise HTTPException(status_code=404, detail='category not found')
        self.db.delete(cat)
        self.db.commit()

    def edit_category(self, req: EditCategoryReq, _id: int):
        category = self.get_category_by_id(_id)
        if category is None:
            raise HTTPException(status_code=404, detail='category not found')
        category.category_name = req.category_name
        self.db.commit()
        return category

    def get_all_by_category(self, _id):
        category = self.get_category_by_id(_id)
        if category is None:
            raise HTTPException(detail='category not found', status_code=404)
        return category.rental_item

    def add_item_to_category(self, _id, req: AddItemToCategoryReq, _account: LoggedInUser) -> models.RentalItem:
        category = self.get_category_by_id(_id)
        if category is None:
            raise HTTPException(status_code=404, detail='category not found')

        rental_item = models.RentalItem(**req.model_dump())
        rental_item.category_category = category
        rental_item.created_at = datetime.datetime.now()
        rental_item.created_by_user_id = _account.auth_user_id
        state = self.db.query(models.RentalItemState).filter(models.RentalItemState.rental_item_state == 'free').first()
        rental_item.rental_item_state_rental_item_state = state
        # if req.serial_number is None or req.serial_number == "":
        # rental_item.serial_number = str(uuid.uuid4())
        # pass
        # else:
        #  rental_item.serial_number = req.serial_number

        self.db.add(rental_item)
        self.db.commit()
        return rental_item


def get_service(db: models.Db):
    return CategoryService(db)


CatServ = Annotated[CategoryService, Depends(get_service)]
