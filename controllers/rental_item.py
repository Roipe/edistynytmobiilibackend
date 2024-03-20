from fastapi import APIRouter, Path, HTTPException

from dependencies import LoggedInUser
from dtos.rental_item import AddFeatureReq, GetItemRes, GetRentalItemFeaturesRes, EditItemReq, RentItemReq
from services.rental_item import RItemServ

router = APIRouter(
    prefix='/api/v1/rentalitem',
    tags=['rental_item']
)


@router.get('/{rental_item_id}')
async def get_item_by_item_id(service: RItemServ, rental_item_id: int = Path(gt=0)) -> GetItemRes:
    item = service.get_item_by_id(rental_item_id)

    return item


@router.get('/{rental_item_id}/features')
async def get_features_by_item(service: RItemServ, rental_item_id: int = Path(gt=0)) -> GetRentalItemFeaturesRes:
    item = service.get_item_by_id(rental_item_id)

    return {'features': item.rental_item_has_rental_item_feature}


@router.post('/{rental_item_id}/rent')
async def rent_item(service: RItemServ, req: RentItemReq, account: LoggedInUser, rental_item_id: int = Path(gt=0)):
    if account is None and req.auth_user_auth_user_id is None:
        raise HTTPException(status_code=401, detail="unauthorized")
    elif account is not None:
        req.auth_user_auth_user_id = account.id
    service.rent_item(rental_item_id, req)
    return ""


@router.put('/{rental_item_id}/features')
async def add_feature_to_item(service: RItemServ, req: AddFeatureReq, rental_item_id: int = Path(gt=0)):
    service.add_feature(rental_item_id, req)


@router.put('/{rental_item_id}')
async def edit_item(service: RItemServ, req: EditItemReq, rental_item_id: int = Path(gt=0)) -> GetItemRes:
    item = service.edit_item(rental_item_id, req)
    return item


@router.delete('/{rental_item_id}')
async def delete_item(service: RItemServ, rental_item_id: int = Path(gt=0)):
    item = service.delete_item_by_id(rental_item_id)
    return item
