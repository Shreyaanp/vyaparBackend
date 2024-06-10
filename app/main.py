from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from .database import init_db
from .auth import register_user, login_user
from .product import upload_product_details, get_user_products
from .s3_utils import upload_file_to_s3, upload_files_to_s3

app = FastAPI()

# Initialize MongoDB
init_db()

# Models
class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

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

# Authentication endpoints
@app.post("/auth/register")
async def register(user: User):
    return await register_user(user)

@app.post("/auth/login")
async def login(login_data: LoginData):
    return await login_user(login_data.email, login_data.password)

# S3 upload endpoints
@app.post("/upload/s3")
async def upload_to_s3(file: UploadFile = File(...)):
    link = upload_file_to_s3(file.file, "your_bucket_name", f"uploads/{file.filename}")
    if not link:
        raise HTTPException(status_code=500, detail="Error uploading file to S3")
    return {"s3_link": link}

@app.post("/upload/s3/multiple")
async def upload_multiple_to_s3(files: list[UploadFile] = File(...)):
    links = upload_files_to_s3(files, "your_bucket_name", "uploads/")
    if not links:
        raise HTTPException(status_code=500, detail="Error uploading files to S3")
    return {"s3_links": links}

@app.post("/upload/s3/generated")
async def upload_generated_to_s3(file: UploadFile = File(...)):
    link = upload_file_to_s3(file.file, "your_bucket_name", f"generated/{file.filename}")
    if not link:
        raise HTTPException(status_code=500, detail="Error uploading generated file to S3")
    return {"s3_link": link}

# Product endpoints
@app.post("/product/upload")
async def upload_product(product: Product):
    return await upload_product_details(product.dict())

@app.get("/product/{user_id}")
async def get_products(user_id: str):
    return await get_user_products(user_id)
