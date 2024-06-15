from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId
from .database import db

class ResponseData(BaseModel):
    ProductRegionalNames: list[str]
    ProductName: str
    ProductDescription: str
    ProductVariation: str
    AboutProduct: list[str]
    ProductTagline: str
    ProductPrompt: str
    MarketPainPoints: list[str]
    CustomerAcquisition: list[str]
    MarketEntryStrategy: list[str]
    SeoFriendlyTags: list[str]

class Product(BaseModel):
    inputLanguage: str
    shopName: str
    sellerState: str
    productlanguage: str
    productCategory: str
    productTitle: str
    pricing: str  # Ensure this matches the type of data you're sending
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
