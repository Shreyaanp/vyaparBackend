from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId
from .database import db

class SellerDetails(BaseModel):
    shop_name: str
    seller_state: str
    product_language: str
    product_category: str

class ProductDetails(BaseModel):
    product_title: str
    pricing: float
    product_description: str = None
    product_variation: str = None

class GeneratedData(BaseModel):
    product_regional_names: list
    product_name: str
    product_description: str
    about_product: list
    product_tagline: str
    product_prompt: str
    seo_friendly_tags: list

class Product(BaseModel):
    user_id: str
    language: str
    seller_details: SellerDetails
    product_details: ProductDetails
    product_image: str
    user_logo: str
    generated_data: GeneratedData

def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid(i) for i in obj]
    return obj

async def upload_product_details(product_dict):
    result = db.products.insert_one(product_dict)
    if result.inserted_id:
        product_dict["_id"] = str(result.inserted_id)
    return {"message": "Product uploaded successfully", "product": convert_objectid(product_dict)}

async def get_user_products(user_id: str):
    products = list(db.products.find({"user_id": user_id}))
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this user")
    return convert_objectid(products)
