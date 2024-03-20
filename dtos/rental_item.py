import datetime
from typing import List, Optional

from pydantic import BaseModel

from dtos.auth import RegisterRes
from dtos.category import Category


class RentalItemByCategory(BaseModel):
    rental_item_id: int
    rental_item_name: str


class GetItemsByCategory(BaseModel):
    items: List[RentalItemByCategory]


class AddItemToCategoryReq(BaseModel):
    rental_item_name: str
    # rental_item_description: Optional[str]
    # serial_number: Optional[str]
    created_by_user_id: Optional[int]


class AddFeatureReq(BaseModel):
    feature_id: int
    value: str


class RentItemReq(BaseModel):
    auth_user_auth_user_id: Optional[int]


class EditItemReq(BaseModel):
    rental_item_name: str


class RentalItemState(BaseModel):
    rental_item_state_id: int
    rental_item_state: str


class GetItemRes(BaseModel):
    rental_item_id: int
    created_by_user: RegisterRes
    category_category: Category
    #serial_number: str
    rental_item_name: str
    created_at: datetime.datetime
    rental_item_state_rental_item_state: RentalItemState
    # rental_item_description: str
    deleted_at: Optional[datetime.datetime]


class RentalItemFeatureName(BaseModel):
    rental_item_feature_name: str


class RentalItemFeature(BaseModel):
    rental_item_feature_rental_item_feature_id: int
    value: str
    rental_item_feature_rental_item_feature: RentalItemFeatureName


class GetRentalItemFeaturesRes(BaseModel):
    features: List[RentalItemFeature]
