from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId
from typing import Dict, Any, List
from .database import db
import uuid

class Product(BaseModel):
    uid: str
    inputLanguage: str
    shopName: str
    sellerState: str
    productlanguage: str
    productCategory: str
    productTitle: str
    pricing: str
    productDescription: str
    productVariation: str
    response: Dict[str, Any]
    companyLogo: str
    images: List[str]

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

async def update_product_details(product_id: str, product: Dict[str, Any]):
    update_result = db.products.update_one({"_id": ObjectId(product_id)}, {"$set": product})
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

async def delete_product_helper(product_id: str):
    delete_result = db.products.delete_one({"_id": ObjectId(product_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

async def publish_product(uid: str, data: Dict[str, Any]):
    try:
        shareable_id = str(uuid.uuid4())
        public_data = {"uid": uid, "data": data, "shareable_id": shareable_id}
        result = db.public.insert_one(public_data)
        if result.inserted_id:
            return {"message": "Product published successfully", "shareable_id": shareable_id}
        else:
            raise HTTPException(status_code=500, detail="Error publishing product")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_public_product(shareable_id: str):
    public_product = db.public.find_one({"shareable_id": shareable_id})
    if not public_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return public_product['data']
