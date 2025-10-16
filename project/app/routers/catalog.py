from typing import List
from fastapi import APIRouter, Depends
from app.models import CatalogProduct
from app.deps import get_user_id


router = APIRouter(prefix="/catalog", tags=["catalog"])


PRESET_PRODUCTS = [
    {"name": "Milk", "category": "Dairy", "preset": "milk"},
    {"name": "Eggs", "category": "Dairy", "preset": "eggs"},
    {"name": "Bread", "category": "Bakery", "preset": "bread"},
    {"name": "Butter", "category": "Dairy", "preset": "butter"},
    {"name": "Cheese", "category": "Dairy", "preset": "cheese"},
    {"name": "Chicken", "category": "Meat", "preset": "chicken"},
    {"name": "Beef", "category": "Meat", "preset": "beef"},
    {"name": "Rice", "category": "Grains", "preset": "rice"},
    {"name": "Pasta", "category": "Grains", "preset": "pasta"},
    {"name": "Tomatoes", "category": "Vegetables", "preset": "tomatoes"},
    {"name": "Onions", "category": "Vegetables", "preset": "onions"},
    {"name": "Potatoes", "category": "Vegetables", "preset": "potatoes"},
    {"name": "Apples", "category": "Fruits", "preset": "apples"},
    {"name": "Bananas", "category": "Fruits", "preset": "bananas"},
    {"name": "Orange Juice", "category": "Beverages", "preset": "orange_juice"},
    {"name": "Coffee", "category": "Beverages", "preset": "coffee"},
    {"name": "Tea", "category": "Beverages", "preset": "tea"},
    {"name": "Sugar", "category": "Pantry", "preset": "sugar"},
    {"name": "Salt", "category": "Pantry", "preset": "salt"},
    {"name": "Olive Oil", "category": "Pantry", "preset": "olive_oil"},
]


@router.get("/products", response_model=List[CatalogProduct])
async def get_catalog_products(user_id: str = Depends(get_user_id)):
    return PRESET_PRODUCTS
