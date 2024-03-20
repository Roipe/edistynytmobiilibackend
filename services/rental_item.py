from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, Depends

import models
from dtos.rental_item import AddFeatureReq, EditItemReq
from services.base import BaseService


class RentalItemService(BaseService):
    def __init__(self, db: models.Db):
        super(RentalItemService, self).__init__(db)

    def get_item_by_id(self, _id) -> models.RentalItem:
        return self.db.query(models.RentalItem).filter(models.RentalItem.rental_item_id == _id).first()

    def get_feature_by_id(self, _id) -> models.RentalItemFeature:
        return self.db.query(models.RentalItemFeature).filter(
            models.RentalItemFeature.rental_item_feature_id == _id).first()

    def add_feature(self, _id, req: AddFeatureReq):
        _item = self.get_item_by_id(_id)

        if _item is None:
            raise HTTPException(status_code=404, detail='item not found')
        feature = self.get_feature_by_id(req.feature_id)

        if feature is None:
            raise HTTPException(status_code=404, detail='feature not found')

        self.db.add(models.RentalItemHasRentalItemFeature(
            value=req.value,
            rental_item_rental_item=_item, rental_item_feature_rental_item_feature=feature))
        self.db.commit()

    def edit_item(self, _id, req: EditItemReq):
        item = self.get_item_by_id(_id)
        if item is None:
            raise HTTPException(status_code=404, detail='item not found')
        item.rental_item_name = req.rental_item_name
        self.db.commit()
        return item

    def rent_item(self, _id, req):
        item = self.get_item_by_id(_id)
        if item is None:
            raise HTTPException(status_code=404, detail='item not found1')
        if item.rental_item_state_rental_item_state.rental_item_state != 'free':
            raise HTTPException(status_code=404,
                                detail='item not found2  ' + item.rental_item_state_rental_item_state.rental_item_state)
        state_id = self.db.query(models.RentalItemState).filter(
            models.RentalItemState.rental_item_state == 'reserved').first().rental_item_state_id
        item.rental_item_state_rental_item_state_id = state_id
        # self.db.commit()
        state_id = self.db.query(models.RentalTransactionState).filter(
            models.RentalTransactionState.rental_transaction_state == 'reserved').first().rental_transaction_state_id
        rental_transaction = models.RentalTransaction(
            created_at=datetime.now(),
            rental_item_rental_item_id=_id,
            auth_user_auth_user_id=req.auth_user_auth_user_id,
            rental_transaction_state_rental_transaction_state_id=state_id

        )

        self.db.add(rental_transaction)
        self.db.commit()

    def delete_item_by_id(self, _id):
        item = self.get_item_by_id(_id)
        if item is None:
            raise HTTPException(status_code=404, detail='item not found')
        self.db.query(models.RentalTransaction).filter(
            models.RentalTransaction.rental_item_rental_item_id == item.rental_item_id).delete()
        self.db.query(models.RentalItemHasRentalItemFeature).filter(
            models.RentalItemHasRentalItemFeature.rental_item_rental_item_id == item.rental_item_id).delete()
        self.db.delete(item)
        self.db.commit()


def get_service(db: models.Db):
    return RentalItemService(db)


RItemServ = Annotated[RentalItemService, Depends(get_service)]
