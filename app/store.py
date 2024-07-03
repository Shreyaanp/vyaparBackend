from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId
from typing import Dict, Any, List
from .database import db
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class ShopAddress(BaseModel):
    flat: str
    street: str
    landmark: str
    district: str
    city: str
    pinCode: str

class SellerInformation(BaseModel):
    name: str
    companyName: str
    aadhar: str
    pan: str
    gst: str
    fassai: str

class SellerDocuments(BaseModel):
    aadhar: str
    pan: str
    addressProof: str
    gst: str

class BankDetails(BaseModel):
    name: str
    accountNum: str
    bankName: str
    ifsc: str

class ProductDetails(BaseModel):
    address: str
    latitude: float
    longitude: float
    Shopaddress: ShopAddress
    title: str
    storeImage: List[str]
    sellerInformation: SellerInformation
    sellerDocuments: SellerDocuments
    bankDetails: BankDetails
    cancelledCheque: str

def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid(i) for i in obj]
    return obj

async def create_store_product(product_dict):
    result = db.store.insert_one(product_dict)
    if result.inserted_id:
        product_dict["_id"] = str(result.inserted_id)
    return {"message": "Product uploaded successfully", "product": convert_objectid(product_dict)}

async def get_store_products(user_id: str):
    products = list(db.store.find({"user_id": user_id}))
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this user")
    return convert_objectid(products)

async def update_store_product(product_id: str, product: Dict[str, Any]):
    try:
        logging.info(f"Updating product with ID {product_id} with data: {product}")
        update_result = db.store.update_one({"_id": ObjectId(product_id)}, {"$set": product})
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product updated successfully"}
    except Exception as e:
        logging.error(f"Error updating product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def delete_store_product(product_id: str):
    delete_result = db.store.delete_one({"_id": ObjectId(product_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
