from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId
from .database import db
from typing import List

class ResponseData(BaseModel):
    ProductRegionalNames: List[str]
    ProductName: str
    ProductDescription: str
    ProductVariation: List[str]
    AboutProduct: List[str]
    ProductTagline: str
    ProductPrompt: str
    MarketPainPoints: List[str]
    CustomerAcquisition: List[str]
    MarketEntryStrategy: List[str]
    SeoFriendlyTags: List[str]

class Product(BaseModel):
    inputLanguage: str
    shopName: str
    sellerState: str
    productlanguage: str
    productCategory: str
    productTitle: str
    pricing: str
    productDescription: str
    productVariation: str
    response: ResponseData
    uid: str

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
    products = list(db.products.find({"uid": user_id}))
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this user")
    return convert_objectid(products)

async def update_product_details(product_id: str, product: Product):
    update_result = db.products.update_one({"_id": ObjectId(product_id)}, {"$set": product.dict()})
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

async def delete_product(product_id: str):
    delete_result = db.products.delete_one({"_id": ObjectId(product_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
