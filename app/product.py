from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId
from .database import db

class ResponseData(BaseModel):
    Product_Regional_Names: list
    Product_Name: str
    Product_Description: str
    Product_Variation: str
    About_Product: list
    Product_Tagline: str
    Product_Prompt: str
    Market_PainPoints: list
    Customer_Acquisition: list
    Market_Entry_Strategy: list
    Seo_Friendly_Tags: list

class Product(BaseModel):
    inputLanguage: str
    shopName: str
    sellerState: str
    productLanguage: str
    productCategory: str
    productTitle: str
    pricing: float
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
    products = list(db.products.find({"user_id": user_id}))
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this user")
    return convert_objectid(products)
