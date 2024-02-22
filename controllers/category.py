from fastapi import APIRouter, Depends, Path

import models
# import old
from dependencies import Admin, require_admin, LoggedInUser
from dtos.category import GetAllCategoriesRes, AddNewCategoryReq, AddNewCategoryRes, EditCategoryReq, GetCategoryRes
from dtos.rental_item import GetItemsByCategory, AddItemToCategoryReq, RentalItemByCategory
from services.category import CatServ

router = APIRouter(
    prefix='/api/v1/category',
    tags=['category']
)


@router.delete('/{category_id}', dependencies=[Depends(require_admin)])
async def remove_category(service: CatServ, category_id: int = Path(gt=0)):
    service.remove(category_id)
    return ""


@router.put('/{category_id}', dependencies=[Depends(require_admin)])
async def edit_category(service: CatServ, req: EditCategoryReq, category_id: int = Path(gt=0)) -> AddNewCategoryRes:
    category = service.edit_category(req, category_id)
    return category


@router.post('/')
async def add_new_category(service: CatServ, req: AddNewCategoryReq) -> AddNewCategoryRes:
    category = models.Category(**req.model_dump())
    service.create(category)
    return category


@router.get('/{category_id}')
async def get_category_by_id(service: CatServ, category_id: int = Path(gt=0)) -> GetCategoryRes:
    category = service.get_category_by_id(category_id)
    return {'category': category}


@router.get('/')
async def get_all_categories(service: CatServ) -> GetAllCategoriesRes:
    categories = service.get_all()
    return {'categories': categories}


@router.get('/{category_id}/items')
async def get_items_by_category(service: CatServ, category_id: int = Path(gt=0)) -> GetItemsByCategory:
    items = service.get_all_by_category(category_id)
    return {'items': items}


@router.post('/{category_id}/items')
async def add_item_to_category(service: CatServ, req: AddItemToCategoryReq,
                               _account: LoggedInUser,
                               category_id: int = Path(gt=0)) -> RentalItemByCategory:
    item = service.add_item_to_category(category_id, req, _account)
    return item
