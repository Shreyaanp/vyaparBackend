from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .database import init_db
from .auth import register_user, login_user
from .product import upload_product_details, get_user_products
from .s3_utils import upload_file_to_s3, upload_files_to_s3, check_s3_connection
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize MongoDB
init_db()

# Check S3 connection
if not check_s3_connection():
    raise RuntimeError("Failed to connect to S3. Check your AWS credentials and network connection.")

# CORS configuration
origins = [
    "http://localhost:5173",
    "https://backend.vlai.in",
    "https://vyaparfrontend.vercel.app",
    # Add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Set specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Health check endpoint
@app.get("/")
async def read_root():
    return {"message": "Server is working"}

# Models
class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

class ResponseData(BaseModel):
    Product_Regional_Names: list
    Product_Name: str
    Product_Description: str
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
    link = upload_file_to_s3(file.file, "vyaparbackend", f"uploads/{file.filename}")
    if not link:
        raise HTTPException(status_code=500, detail="Error uploading file to S3")
    return {"s3_link": link}

@app.post("/upload/s3/multiple")
async def upload_multiple_to_s3(files: list[UploadFile] = File(...)):
    links = upload_files_to_s3(files, "vyaparbackend", "uploads/")
    if not links:
        raise HTTPException(status_code=500, detail="Error uploading files to S3")
    return {"s3_links": links}

@app.post("/upload/s3/generated")
async def upload_generated_to_s3(file: UploadFile = File(...)):
    link = upload_file_to_s3(file.file, "vyaparbackend", f"generated/{file.filename}")
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

from fastapi import HTTPException
from bson import ObjectId
from .database import db

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
